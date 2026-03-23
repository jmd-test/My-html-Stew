import requests as r
html_test = "<html><div><test><img/></test><div><p>hello</p><p>2nd text!!!</p></div></div></html>"

#side functions like error handling or displaying

def error(error_text):
    print(error_text)
    n = 0
    while True:
        n += 0.00001

#main parser functions

def split_anglebrackets(url):
    print("splitting...")
    messy_html = r.get(url)
    messy_html = [*("".join(messy_html.text))]
    if True == False: #make it true if you wanna test the 'html_test' variable!!!
        messy_html = html_test
    fetching_tag = False
    formed_word = []
    kinda_messy_html = []
    n = 0
    for char in messy_html:
        if not fetching_tag:
            if char == "<":
                if formed_word != []:
                    kinda_messy_html.append("".join(formed_word).strip())
                    formed_word = []
                    formed_word.append(char)
                    fetching_tag = True
                else:
                    formed_word.append(char)
                    fetching_tag = True
            else:
                formed_word.append(char)
        elif fetching_tag:
            if char == ">":
                formed_word.append(char)
                kinda_messy_html.append(("".join(formed_word)).replace("\n",""))
                formed_word = []
                fetching_tag = False
            else:
                formed_word.append(char)
        n += 1
    print("finished splitting")
    return kinda_messy_html
    


def get_tag_name(html_string):
    html_string = [*html_string]
    tag_type = ""
    if html_string[1] == "/":
        tag_type = "closing"
        html_string = html_string[2:len(html_string)]
    else:
        tag_type = "opening"
        html_string = html_string[1:len(html_string)]
    tag_formed = []
    for char in html_string:
        if char == " " or char == "/" or char == ">":
            if html_string[-2] == "/":
                tag_type = "void"
            #67 67676767 67
            if "".join(tag_formed) in ["meta", "link", "img", "br", "hr", "input", "area", "base", "col", "embed", "source", "track", "wbr"]:
                tag_type = "void" #SAIS SHETE
            return tag_type,"".join(tag_formed)
        else:
            tag_formed.append(char)
    
    
    
def get_tag_attrs(tag_type,tag_name,html_string):
    tag_moe = len([*html_string]) - len([*tag_name]) #moe stands for Margin Of Error!
    if tag_moe < 4 or tag_type == "closing":
        has_attr_bool = False
        return "".join(tag_type) + " " + "".join(tag_name), has_attr_bool
    else:
        has_attr_bool = True
        html_string = [*html_string]
        if tag_type == "void":
            html_string = html_string[0:(len(html_string) - 2)]
        isolated_attrs = html_string[(len([*tag_name]) + 2):len(html_string)]
        
        getting_name = True
        getting_data = False
        reached_eq = False
        formed_name = []
        formed_data = []
        attributes = []
        for char in isolated_attrs:
            if (char == '"' or char == "'" or char == ">") and formed_data != [] and getting_data:
                if char != " " and char != ">":
                    formed_data.append(char)
                formed_data = "".join(formed_data)
                formed_name = "".join(formed_name)
                attributes.append([tag_name,"attr_name",formed_name])
                attributes.append([tag_name,"attr_data",formed_data])
                formed_data = []
                formed_name = []
                getting_data = False
                
            if char != " " and not getting_name and not getting_data and not reached_eq:
                getting_name = True
            if getting_data:
                formed_data.append(char)
            if char == " " or char == "=" and getting_name:
                getting_name = False
            if getting_name:
                formed_name.append(char)
            if char == "=" and not getting_name:
                reached_eq = True
            if (char != " " or char == '"' or char == "'") and char != "=" and reached_eq:
                reached_eq = False
                getting_data = True
                formed_data.append(char)
        return attributes, has_attr_bool
        
    
    
def resolve_bracket_cases(km_html):
    print("resolving cases and attrs...")
    tag_stack = ["GLOBAL_TAG"]
    sorta_messy_html = []
    for tag in km_html:
        if tag.startswith("<"):
            tag_type, tag_name = get_tag_name(tag)
            tag_full, has_attr = get_tag_attrs(tag_type,tag_name,tag)
            if has_attr:
                tag_full = list(tag_full)
                tag_full.insert(0,tag_name)
                tag_full.insert(0,tag_type)
            else:
                tag_full = tag_full.split(" ")
            if tag_type == "opening":
                tag_stack.append(tag_name)
            elif tag_type == "closing":
                tag_name = tag_stack.pop()
            sorta_messy_html.append(tag_full)
        else:
            sorta_messy_html.append([tag_stack[-1].strip(), "contents" ,tag])
    return sorta_messy_html



# main tree growing things!!!!!!!!! ○■■○■○■■○■○■○■○○■■○■■○■○■○■○■○○■○■○■○■■○■○■○■○■■○○■○■■○○■○■■○○■■○■○○■○■○○■■○○○○■○■○■○■■○■○■○■○■■○■○■○■

def get_tree_seeds(sm_html):
    print("getting seeds...")
    tree_seeds = []
    tag_attributes = []
    for object in sm_html:
        if object[0] == "opening":
            tree_seeds.append(["make parent:",object[1]])
            if len(object) > 2:
                tag_attributes = object[2:len(object)]
                for attribute_node in tag_attributes:
                    tree_seeds.append([attribute_node[1],attribute_node[2]])
        if object[0] == "closing":
            tree_seeds.append(["pop parent:",object[1]])
        if object[0] == "void":
            if len(object) > 2:
                seed_has_attr = True
                tree_seeds.append(["singular object:",object[1],seed_has_attr])
                tag_attributes = object[2:len(object)]
                for attribute_node in tag_attributes:
                    tree_seeds.append([attribute_node[1],attribute_node[2]])
                tree_seeds.append(["end of S.O attrs:",object[1]])
            else:
                seed_has_attr = False
                tree_seeds.append(["singular object:",object[1],seed_has_attr])
        if object[1] == "contents":
            tree_seeds.append(["contents:",object[2]])
    return tree_seeds
                
                

def grow_tree(sm_html):
    print("starting tree growing...")
    tree_seeds = get_tree_seeds(sm_html)
    
    global FATHER_brick
    FATHER_brick = brick("GLOBAL_TAG","no papa")
    
    global tree_tag_stack
    tree_tag_stack = [FATHER_brick]
    
    attr_name = ""
    attr_name_pointer = None
    fetching_so_attrs = False
    
    while tree_seeds[0][0] != "make parent:":
        tree_seeds.pop(0)
    if tree_seeds[0][1] == "!DOCTYPE":
        del tree_seeds[0:2]
    
    for seed in tree_seeds:
        if seed[0] == "make parent:":
            tree_brick = brick(seed[1],tree_tag_stack[-1])
            tree_tag_stack[-1].brick_babies.append(tree_brick)
            tree_tag_stack.append(tree_brick)
        if seed[0] == "attr_name":
            tree_tag_stack[-1].brick_attrs[seed[1]] = ""
            attr_name = seed[1]
            attr_name_pointer = tree_tag_stack[-1]
        if seed[0] == "attr_data":
            attr_name_pointer.brick_attrs[attr_name] = seed[1]
        if seed[0] == "contents:":
            tree_brick = brick(seed[1],tree_tag_stack[-1])
            tree_brick.brick_data = seed[1]
            tree_tag_stack[-1].brick_data = seed[1]
        if seed[0] == "singular object:":
            tree_brick = brick(seed[1],tree_tag_stack[-1])
            tree_tag_stack[-1].brick_babies.append(tree_brick)
            if seed[2] == True:
                fetching_so_attrs = True
                tree_tag_stack.append(tree_brick)
        if seed[0] == "end of S.O attrs:" and fetching_so_attrs:
            tree_tag_stack.pop()
        if seed[0] == "pop parent:":
            tree_tag_stack.pop()
    print("tree done growing!!!")
    return tree_seeds

# the brick class hahahhaa ■■■■●●●●□□□□□■■■■■□□□□□■■■■■■□□□□□□■■■■■□□□□□■■■■■□□□□□■■■■■□□□□□□■■■■■■□□□□□□■■■■■■□□□□□□■■■■■■□□□□□■■■■■■□□□□□□■■■■■■

class brick:
    def __init__(self,brick_name,brick_parent):
        self.brick_name = brick_name
        self.brick_parent = brick_parent
        self.brick_data = ""
        self.brick_babies = []
        self.brick_attrs = {}

# TREE SCAVENGING FUNCTIONSSS

def stabilize_list(chaotic_list):
    flat = True
    disciplined_list = []
    for item in chaotic_list:
        if type(item) == type("testicle"):
            disciplined_list = chaotic_list
            break
        try:
            disciplined_list.extend(item)
        except:
            disciplined_list.append(item)
    for item in disciplined_list:
        if isinstance(item,list):
            flat = False
            break
    if not flat:
        disciplined_list = stabilize_list(disciplined_list)
        return disciplined_list
    else:
        return disciplined_list
       


def get_brick_attribute(parent,attribute_code,raw_bool):
    if attribute_code == "name":
        if raw_bool:
            return parent
        else:
            return parent.brick_name
    if attribute_code == "parent":
        if raw_bool:
            return parent.brick_parent
        else:
            return parent.brick_parent.brick_name
    if attribute_code == "data":
        if raw_bool:
            print("'raw' has no effect for data attributes")
        return parent.brick_data
    if attribute_code == "babies":
        babies = parent.brick_babies
        babies = babies[:]
        if raw_bool:
            return babies
        else:
            n = 0
            while n != len(babies):
                babies[n] = babies[n].brick_name
                n += 1
            return babies
    if attribute_code == "attributes":
        if raw_bool:
            print("'raw' has no effect for attributes of a tag")
        return parent.brick_attrs
    return "this attribute doesnt exist!!!"



def versatile_find(parent,tag_name,attribute,raw_bool,find_all_bool):
    babies_pointer = parent.brick_babies
    babies_names = []
    result_bunched = [] #can be used ONLY for find_all, okay!!!
    found_tag_bool = False #only used if using 'find' instead of 'find all' so dont worry!!!
    infertile_parents = ["meta", "link", "img", "br", "hr", "input", "area", "base", "col", "embed", "source", "track", "wbr"]
    n = 0
    while n != len(babies_pointer):
        converted_name = babies_pointer[n].brick_name
        babies_names.append(converted_name)
        n += 1
    
    if not find_all_bool:
        if tag_name == parent.brick_name:
            result = get_brick_attribute(parent,attribute,raw_bool)
            return result,True
        else:
            if len(babies_pointer) == 0:
                return "no match", False
            for baby in babies_pointer:
                result, found_tag_bool = versatile_find(baby,tag_name,attribute,raw_bool,find_all_bool)
                if found_tag_bool:
                    return result,True
            return "no match found", False
    elif find_all_bool:
        if len(babies_pointer) != 0:
            for baby in babies_pointer:
                result = versatile_find(baby,tag_name,attribute,raw_bool,find_all_bool)
                if type(result) == type(None) or result == []:
                    pass
                else:  
                    result_bunched.append(result)
            if parent.brick_name == tag_name:
                result = get_brick_attribute(parent,attribute,raw_bool)
                result_bunched.append(result)
            return stabilize_list(result_bunched)
        else:
            if parent.brick_name == tag_name:
                result = get_brick_attribute(parent,attribute,raw_bool)
                return result
            
#the MessyStew library yayyyy!!!!!!!!

class MessyStew:
    def __init__(self,url):
        self.messy_ass_stew = grow_tree(resolve_bracket_cases(split_anglebrackets(url)))
    def find(self,tag_name,brick_attribute="babies",raw=False):
        find_result,bool_byproduct = versatile_find(FATHER_brick,tag_name,brick_attribute,raw,False)
        return find_result
    def find_all(self,tag_name,attribute="babies",raw=False):
        find_all_result = versatile_find(FATHER_brick,tag_name,attribute,raw,True)
        return find_all_result

#test stuff HERE PLEASE ■■■■■■■■■■■■■■■■ 
p = MessyStew("https://github.com")
n = p.find_all("p",attribute="data")
print(n)
n = p.find_all("div",attribute="babies",raw=False)
print(n)