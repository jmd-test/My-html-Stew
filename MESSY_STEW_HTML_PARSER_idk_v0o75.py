import requests as r
html_test = "<html><div><a>hi nigeria</a></div><img src='https link' alt='haha u blind'/>test</html>"

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
    if 1 == 2:
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
            if "".join(tag_formed) == "link" or "".join(tag_formed) == "meta":
                tag_type = "void"
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

# TREE SCAVENGING FUNCTIONS AND CLASS!●■●■○□○□○●■●■○□○□●■●■○□○□●■●■○□○□○■●■●■○□○□○■●■●■○□○□○

def scavenge_babies(starting_parent,tag_name,brick_attribute):
    the_brick_babies = starting_parent.brick_babies
    brick_babies_names = the_brick_babies[:]
    infertile_bricks = ["br","img","meta","link","link","img","br","hr","input","area","base","col","embed","source","track","wbr"]
    n = 0
    
    while n != len(the_brick_babies):
        brick_babies_names[n] = the_brick_babies[n].brick_name
        n += 1
    
    if tag_name in brick_babies_names:
        if brick_attribute == "name":
            attribute = (the_brick_babies[(brick_babies_names.index(tag_name))]).brick_name
        if brick_attribute == "parent":
            attribute = (the_brick_babies[(brick_babies_names.index(tag_name))]).brick_parent
        if brick_attribute == "data":
            attribute = (the_brick_babies[(brick_babies_names.index(tag_name))]).brick_data
        if brick_attribute == "babies":
            attribute = (the_brick_babies[(brick_babies_names.index(tag_name))]).brick_babies
            attribute_names = attribute[:]
            n = 0
            for pointer in attribute:
                attribute_names[n] = pointer.brick_name
                n += 1
            attribute = attribute_names[:]
        if brick_attribute == "attributes":
            attribute = (the_brick_babies[(brick_babies_names.index(tag_name))]).brick_attrs
        return attribute, True
    else:
        if brick_babies_names == []:
            return "No babies", False
        for baby in the_brick_babies:
            if baby.brick_name in infertile_bricks:
                pass
            attribute, found_tag = scavenge_babies(baby,tag_name,brick_attribute)
            if found_tag:
                return attribute, True
        if not found_tag:
            return "No match", False
    
class MessyStew:
    def __init__(self,url):
        self.messy_ass_stew = grow_tree(resolve_bracket_cases(split_anglebrackets(url)))
    def find(self,tag_name,brick_attribute):
        result, bool = scavenge_babies(FATHER_brick,tag_name,brick_attribute)
        return result

#test stuff HERE PLEASE ■■■■■■■■■■■■■■■■ 
p = MessyStew("https://github.com")
print(p.find("link","attributes"))
print(p.find("p","data"))
