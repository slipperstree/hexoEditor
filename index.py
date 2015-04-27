import web
import os
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/create', 'create',
    '/edit', 'edit',
    '/update', 'update',
    '/gen_deploy', 'gen_deploy'
)

hexoRoot = '/home/pi/hexo_root'

postDir = hexoRoot + '/source/_posts/'

def execHexoG(newTitle):
    return

def getWzList():
    # Make list for show
    wzList = []
    idx = 0;
    for lists in os.listdir(postDir): 
        path = os.path.join(postDir, lists) 
        if os.path.isfile(path):
            wzList.append([os.path.basename(path), 'wz_'+str(idx)])
            idx = idx + 1
    wzList.sort(reverse=True)
    return wzList


class index:
    def GET(self):
        return render.index(getWzList(), os.getlogin())

class create:
    def POST(self):
        # get the new title
        i = web.input()
        sNewTitle = i.get('text-new-title')
        
        # Get into Hexo dir
        sWebpyDir = os.getcwd()
        os.chdir(hexoRoot)
        
        # Hexo n ...
        os.system('hexo n ' + sNewTitle)
        
        # Return webpy base dir
        os.chdir(sWebpyDir)
        
        # Read new file content
        # Get file name
        # Get today date
        now = datetime.datetime.now()
        filename = now.strftime('%Y-%m-%d-') + sNewTitle + '.md'
        fileHandle = open ( postDir + filename )
        fileContent = fileHandle.read()
        fileHandle.close()
        
        return render.create(sNewTitle, fileContent)

class edit:
    def POST(self):
        # Read file content
        i = web.input()
        fileName = i.get('filename')
        
        fileHandle = open ( postDir + fileName )
        fileContent = fileHandle.read()
        fileHandle.close()
        
        return render.edit(fileName, fileContent)

class update:
    def POST(self):
        # Read file content
        i = web.input()
        fileName = i.get('filename')
        content = i.get('content')
        
        fileHandle = open ( postDir + fileName, 'w' )
        fileHandle.write(content)
        fileHandle.close()
        
        return render.edit(fileName, content)

class gen_deploy:
    def POST(self):
        # Get into Hexo dir
        sWebpyDir = os.getcwd()
        os.chdir(hexoRoot)
        
        # Hexo g ...
        os.system('hexo g')
        
        # Hexo d ...
        os.system('hexo d')
        
        # Return webpy base dir
        os.chdir(sWebpyDir)
        
        return render.index(getWzList())

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()