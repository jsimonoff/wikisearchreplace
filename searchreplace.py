#!/usr/bin/python
#
import re,sys,argparse
from xmlrpclib import Server
"""
Search and replace.

Uses Python regex to do search and replace on a series of pages.

The search and replace strings can be specified in two ways:
1) Explicitly as a string.
2) As a space-key:page-name. The contents of the page is then used as search or replace strings.
Note that the way the program recogizes this is a page reference is by looking for the ":" -- therefore, you can't use a colon if you are
specifying either the search or replace string explictly.  

The pages to be acted on can be specified in four ways.  In all cases, all pages must be in the same space, which is specified with the --key
argument (-k). 
1) As an explicit list of pages separated by spaces (each page name in quotes) with the --titles (-t) argument. 
2) As descendents of a head page specified with the --parent (-f) argument.
3) All pages in a space (if no page list of parent specified).
4) Via a label (all pages pulled from the one specified space, though) specified by the --label (-l) option (may allow multiple labels), which would be OR'd)
5) Page name contains: Gets all pages in space, and operates only on pages containing the text in the string.
"""
WIKI="https://one.rackspace.com"
SPACE='Linux'
COMMENT={'versionComment':"Page reformatted by script."}
############  Arguments ############
argparser = argparse.ArgumentParser(description="Searches for specified page text and replaces with specified replacement.")
argparser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
argparser.add_argument("-s", "--search",required=True, help="Either a string to search for, or a space key:page name string.  If a search string, can't contain ':'.\
In either case, the content is treated as a Python regular expression.",
                    action="store")
argparser.add_argument("-r", "--replace",required=True, help="Either a string to use as a replacement, or a space key:page name string.  If a replacement string, can't contain ':'.\
In either case, the content is treated as a Python regular expression.",
                    action="store")
argparser.add_argument("-w", "--wiki", help="run using this wiki URL (defaults to the One wiki)",
                    action="store")
argparser.add_argument("-u", "--username", help="a wiki username",required=True,
                    action="store")
argparser.add_argument("-p", "--password", help="the password",required=True,
                    action="store")
argparser.add_argument("-l", "--label", help="if supplied, this label is used to identify target pages ",
                    action="store")
argparser.add_argument("-k", "--key", help="if supplied, only applies to pages from the space with this key(if only this\
option is given, then it applies to all pages in the space",
                    action="store")
argparser.add_argument("-f", "--parent", help="if supplied, targets all descendents of this page ",
                    action="store")
argparser.add_argument("-t", "--titles", help="if supplied, lists target pages; must be used with --space to identify the space",nargs='+',
                    action="store")
argparser.add_argument("-i", "--in-title", help="looks for this string to identify titles to act on",
                    action="store")
argparser.add_argument("-c", "--comment", help="a comment to describe the change ",
                    action="store")
args = argparser.parse_args()
if args.wiki:
  if args.verbose: print "wiki",args.wiki
  WIKI=args.wiki 
if args.key:
  if args.verbose: print "space key",args.key
  SPACE=args.key
if args.comment:
  COMMENT={'versionComment':args.commment}
#####################################
def generatePageList():
  pages=[]
  if args.label:
    #Execute get page by label
    if args.verbose: print "Setting up contentbylabel macro"
    macro='<ac:structured-macro ac:name="contentbylabel"><ac:parameter ac:name="spaces"><ri:space ri:space-key="' + SPACE + '" /></ac:parameter><ac:parameter ac:name="showLabels">false</ac:parameter><ac:parameter ac:name="max">9999</ac:parameter><ac:parameter ac:name="labels">' + args.label + '</ac:parameter><ac:parameter ac:name="showSpace">false</ac:parameter></ac:structured-macro>'
    rpage=s.confluence2.getPage(token,"misc","renderpage")
    rpage['content']=macro
    rpage=s.confluence2.storePage(token,rpage)
    opts={'style':'clean'}
    render=s.confluence2.renderContent(token,"",rpage['id'],"",opts)
    plist=render.split('href="')
    plist.pop(0) #throw away first -- now each list item begins with a URL
    for p in plist:
      end=p.index('"')
      url=p[:end]
      #May have space/page or pages/viewpage.action>pageId=somenum
      if 'pageId' in url: #This is the viewpage form, with an ID -- need to get title
        equal=url.index('=')
        tpage=s.confluence2.getPage(token,url[equal+1:])
        pages.append(tpage['title'])
      else:
        pages.append(re.sub("/.*?/.*?/","",url).replace('+',' ').replace('%3A',':').replace('%2C',',')) #Just need the page name, but need to un-encode it (may need more)
  elif args.parent:
    #Get this page, then get its descendents
    topPage=s.confluence2.getPage(token,SPACE,args.parent)
    pagesums=s.confluence2.getDescendents(token,topPage['id'])
    for pagesum in pagesums:
      pages.append(pagesum['title'])
  elif args.titles:
    return args.titles
  else:
    pagesums=s.confluence2.getPages(token,SPACE)
    for pagesum in pagesums:
      pages.append(pagesum['title'])
  return pages
# main program
# Set up confluence
s=Server(WIKI+"/rpc/xmlrpc")
token=s.confluence2.login(args.username,args.password)
pages = generatePageList()
# Set up search and replace values
if args.search and args.replace:
  if ":" in args.search: # This is a page
    searchPageSpec=args.search.split(":") # 0 is space key; 1 is page name
    searchPage=s.confluence2.getPage(token,searchPageSpec[0],searchPageSpec[1])
    search=searchPage['content']
  else:
    search=args.search
  if ":" in args.replace: # This is a page
    replacePageSpec=args.replace.split(":") # 0 is space key; 1 is page name
    replacePage=s.confluence2.getPage(token,replacePageSpec[0],replacePageSpec[1])
    replace=replacePage['content']
  else:
    replace=args.replace
else:#This should never happen -- search and replace args are required
  print "Didn't get required search or replace argument."
  sys.exit(0)
for pagename in pages:
  if args.in_title and args.in_title not in pagename:
    continue
  else:
    if args.verbose: print pagename
    try:
      page=s.confluence2.getPage(token,SPACE,pagename)
      if args.verbose: print "Doing page",pagename.encode('utf8','replace')
    except:
      print "Couldn't read page",pagename
      continue
    oldContent=page['content']
    page['content'] = re.sub(search,replace,page['content'])
    if page['content']==oldContent:
      if args.verbose: print "No changes"
    else:
      page=s.confluence2.updatePage(token,page,COMMENT)
      if args.verbose: print pagename,"HAS BEEN CHANGED"

