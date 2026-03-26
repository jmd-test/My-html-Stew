import requests

def html_tokenizer(url):
    html = requests.get(url)
    html = html.content
    html = str(html).replace("\\n","")
    html = html.replace("\\r","")
    html = html.replace("\\t","")
    getting_tag = False
    getting_content = True #set to TRUE in default cus sometimes code is weird and theres content at the very start
    in_script = False
    formed_token = []
    list_of_tokens = []
    html = [*html]
    for index,character in enumerate(html):
        if not in_script:
            if character == "<":
                try:
                    if formed_token[0] != " ":
                        list_of_tokens.append("".join(formed_token).strip())
                        formed_token = []
                except:
                    if formed_token != []:
                        list_of_tokens.append("".join(formed_token).strip())
                        formed_token = []
                getting_tag = True
                getting_content = False
                formed_token.append(character)
            elif character == ">":
                getting_tag = False
                getting_content = True
                formed_token.append(character)
                list_of_tokens.append("".join(formed_token).strip())
                tag_name = get_name(list_of_tokens[-1])
                tag_type = get_type(tag_name,list_of_tokens[-1])
                if tag_name in ["script","style"] and tag_type == "OPEN":
                    in_script = True
                formed_token = []
            elif getting_tag or getting_content:
                formed_token.append(character)
        elif in_script: #special "loose dumb dumb" mode for when we're in a script tag! neat!!!
            check_a = "".join(html[index:index+9])
            check_b = "".join(html[index:index+8])
            if check_a == "</script>":
                script = "".join(formed_token).strip()
                if [*script] != []:
                    list_of_tokens.append(script)
                formed_token = []
                formed_token.append(character)
                in_script = False
                getting_tag = True
                getting_content = False
                pass
            elif check_b == "</style>":
                script = "".join(formed_token).strip()
                if [*script] != []:
                    list_of_tokens.append(script)
                formed_token = []
                formed_token.append(character)
                in_script = False
                getting_tag = True
                getting_content = False
                pass
            else:
                formed_token.append(character)
    return list_of_tokens

def make_seeds(html_tokens): #seeds are what the tree-builder uses as easy instructions to make THE TREE, simple logic right?
    html_seeds = []
    for token in html_tokens:
        if token.startswith("<"):
            if token.startswith("<!--"):
                pass
            elif token.startswith("<!"):
                pass
            else:
                tag_name = get_name(token)
                tag_type = get_type(tag_name,token)
                tag_attrs = get_attributes(tag_name,token)
                seed = [tag_type,tag_name]
                if (not tag_attrs == "no attributes" and not tag_attrs == {}):
                    seed.append(tag_attrs)
                else:
                    seed.append("no attributes")
                html_seeds.append(seed)
        else:
            html_seeds.append(["CONTENT",token])
    return html_seeds
    
def get_type(tag_name,token): #this mf is unfinished but it works for most cases! 'comment'-type tags are a real pain to figure out though....
    void_tags = ["area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"]
    tag_type = ""
    if tag_name in void_tags or token.endswith("/>"):
        tag_type = "VOID"
    elif token.startswith("</"):
        tag_type = "CLOSE"
    elif token.startswith("<!"):
        if token.startswith("<!--"):
            tag_type = "COMMENT START"
        else:
            tag_type = "DECLARATION"
    else:
        tag_type = "OPEN"
    return tag_type

def get_name(token): #gets the name of a tag, warning, FOR A !!!TAG!!!
    formed_name = []
    if token.startswith("</"):
        token = token[1:]
    for character in token[1:]:
        if character == " " or character == ">":
            return "".join(formed_name) #returns if we hit a space character, which indicates tag name is done!
        else:
            formed_name.append(character)

def get_attributes(token_name,token): #gets the attributes of a tag, has a failsafe for "no attributes", but please give the correct name, and the FULL TAG
    moe = len(token) - len(token_name)
    if moe < 3:
        return "no attributes"
    if token.endswith("/>"):
        token = token[2+len(token_name):len(token)-2] #used when the token has a /> ending, for void tags yeah
    else:
        token = token[2+len(token_name):len(token)-1] #used for normal tags
    formed_word = []
    uncompiled = []
    in_quotes = False
    quote_used = ""
    for index,character in enumerate(token):
        if not in_quotes: #splits tags into non-classified tokens, aware of quotes! cool!!
            if (character in [" ","="] and formed_word != []) or index == len(token)-1:
                if (not character == " ") and index == len(token)-1:
                    formed_word.append(character)
                uncompiled.append("".join(formed_word))
                formed_word = []
            elif not character in [" ","=",'"',"'"]:
                formed_word.append(character)
            elif character in ['"',"'"]:
                quote_used = character
                in_quotes = True
        elif in_quotes:
            if character == quote_used:
                uncompiled.append("".join(formed_word))
                formed_word = []
                in_quotes = False
            else:
                formed_word.append(character)
    titles_list = []
    data_list = []
    for index,token in enumerate(uncompiled): #this little thing splits the "titles" and "data" of the attributes into lists! its a nice buddy to have
        if index % 2 == 0:
            titles_list.append(token)
        else:
            data_list.append(token)
    return dict(zip(titles_list,data_list))

#this is the main node type object!! im loyal to the idea of calling them 'bricks' to be unique though
        
def parse_seeds(html_seeds):
    global genesis_brick
    genesis_brick = brickify("adam the brick")
    seed_stack = [genesis_brick]
    for seed in html_seeds:
        if seed[0] == "OPEN":
            brick = brickify(seed[1]) #sets up the bricks name
            brick.type = "OPEN"
            brick.parent = seed_stack[-1] #sets up the bricks parent
            seed_stack[-1].babies.append(brick) #calls the parent and makes this brick a baby of it
            if len(seed) > 2: #if its greater than 2, it means the seed has an attribute!
                brick.attributes = seed[2] #adds the attribute to the brick (if the condition was met)
            seed_stack.append(brick) #and finally, it adds itself on the top of the stack to be the parent of the next brick, cycle of life!!
        if seed[0] == "CLOSE":
            seed_stack.pop() #easy stuff, really, just pops the parent because the tag is closed!
        if seed[0] == "VOID":
            brick = brickify(seed[1]) #sets up the bricks name
            brick.type = "VOID"
            brick.parent = seed_stack[-1] #sets up the bricks parent
            brick.babies.append("cant have babies") #notice how most of the code is the same? it legit is just an opening seed but infertile
            seed_stack[-1].babies.append(brick) #calls the parent and makes this brick a baby of it
            if len(seed) > 2: #if its greater than 2, it means the seed has an attribute!
                brick.attributes = seed[2] #adds the attribute to the brick (if the condition was met)
        if seed[0] == "CONTENT":
            seed_stack[-1].content = seed[1] #awesomely simple right?? 'content' is such a goat seed, just have to be stuck with the right tag!

class brickify:
    def __init__(self,name,attributes={}):
        self.name = name
        self.attributes = attributes or {}
        self.parent = None
        self.babies = []
        self.content = ""
        self.type = ""

html = make_seeds(html_tokenizer("https://github.com"))
parse_seeds(html)
def show_tree(parent,depth=0,targets=[]):
    indent = "   " * depth
    highlight = ""
    if parent.name in targets:
        highlight = "■○■"
        indent = indent[:len(indent)-3]
    print(highlight,depth,indent,f"<{parent.name} {parent.attributes}>")
    if not parent.content == "":
        print(highlight,depth,indent,parent.content)
    if parent.babies == [] or not parent.babies[0] == "cant have babies":
        for baby in parent.babies:
            show(baby,depth+1,targets)
    else:
        return
    
show_tree(genesis_brick,targets=["script"]) #we use the genesis as a parebt, which in turn loads the ENTIRE TREE, thats cool as hell!
