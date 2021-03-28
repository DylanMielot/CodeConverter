#!/usr/bin/env python
# coding: utf-8

APIS = ["AOPAL", "WOPAL"]

class CodeConverter:
    
    def __init__(self, apis=APIS):
        
        self.sources = {}
        self.indent = 0

        for api in APIS:
            self.sources[api] = ""
        
        
    def wrap_code(f):

        def _(*args, only=APIS, exclude=[], **kwargs):

            self = args[0]
            codes = f(*args, **kwargs)

            for api in self.sources:
                if api in only and api not in exclude:
                    self.sources[api] += " " * self.indent * 4
                    self.sources[api] += codes[api]

        return _
        
        
    def wrap_codeindent(f):

        def _(*args, only=APIS, exclude=[], **kwargs):

            self = args[0]
            f(*args, **kwargs)            
            self.indent += 1

        return _
        
        
    def wrap_codeunindent(f):

        def _(*args, only=APIS, exclude=[], **kwargs):
            
            self = args[0]
            self.indent -= 1
            f(*args, **kwargs)

        return _


    @wrap_code
    def Import(self, libName, path=''):

        return {
            "AOPAL" : "#include "+libName+ ".h; \n",
            "WOPAL" : "import { " +libName+" } from '"+path+"'; \n"
        }

    @wrap_code
    def create_class(self, className, varName, *args):

        params = ", ".join(args)

        return {
            "AOPAL" : className+' '+varName+'('+params+'); \n',
            "WOPAL" : 'var '+varName+ ' = new '+className+'('+params+'); \n'
        }

    @wrap_code    
    def call_method(self, varName, method, *args):

        if len(args)>0:
            params = ", ".join(args)
        else: params = ""

        return {
            "AOPAL" :  varName+"."+method+"("+params+"); \n\n",
            "WOPAL" : varName+"."+method+"("+params+"); \n\n"
        }

    @wrap_code
    def comment(self, comment):

        return {
            "AOPAL" :  "\n /* " + comment + " */ \n",
            "WOPAL" : "\n /* " + comment + " */ \n"
        }
    
    @wrap_codeindent
    @wrap_code
    def start_function(self, funcName, *args, **kwargs):
        
        if len(args)>0:
            params = ", ".join(args)
        else: params = ""
        
        return {
            "AOPAL" :  "void "+funcName+"("+params+"){\n\n",
            "WOPAL" : "function "+funcName+"("+params+"){\n\n"
        }
    
    @wrap_codeunindent
    @wrap_code
    def end_function(self, *args, **kwargs):
        
        return {
            "AOPAL" :  "}\n\n",
            "WOPAL" : "}\n\n"
        }
    
    @wrap_code
    def return_function(self, content, *args, **kwargs):
        
        return {
            "AOPAL" :  "return "+content+"\n",
            "WOPAL" : "return "+content+"\n"
        }
        


################################################
########## Code to be converted ################
################################################

code = CodeConverter()

code.Import("Opal", "../opal.js")
code.Import("OpalBlock", "../opal.js", only=["AOPAL"])

code.comment("Initialize Opal instance")

code.create_class("Opal", "Opal")
code.call_method("Opal", "Init")

code.create_class("OpalBlock", "greyCircle")
code.call_method("greyCircle", "Init")

code.create_class("OpalTexture", "Tex1")
code.call_method("Tex1", "Init")

code.call_method("greyCircle", "setOutputTexture", "Tex1")

#start function
code.start_function("test_greyCircle", "greyCircle", "Opal")
code.call_method("greyCircle", "render")
code.end_function()


print("AOPAL : \n")
print(code.sources['AOPAL'], "\n\n")
print("WOPAL : \n")
print(code.sources['WOPAL'])


################################################
################# JS Example ###################
################################################

code = CodeConverter(apis=["WOPAL"])


code.comment("Hello world")

#start function
code.start_function("hello")
code.return_function("'Hello'")
code.end_function()


# In[127]:


with open("build_js/index.js", "w") as file:
    file.write(code.sources["WOPAL"])

HTML = """
<html>
<body>

    <h1 id='title'> </h1>
    
    <script src="index.js"></script>
    
    <script>
        document.getElementById('title').innerHTML = hello();
    </script>
    
</body>
</html>
"""

with open("build_js/index.html", "w") as file:
    file.write(HTML)

import os
os.system("build_js\\index.html")


# In[ ]:




