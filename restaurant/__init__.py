import re

def comma_splitter(tag_string):
    t_list= [t.strip().lower() for t in tag_string.split(',') if t.strip()]
    regex = re.compile('[-]')
    t_list_new=[]
    for t in t_list:
        tag=t
        tag_new=""
        if regex.search(tag)==None:
        	tag=tag.strip('\"')
        	t_list_new.append(tag)
        else:
            new_tag=tag.replace("-"," ")
            t_list_new.append(new_tag)
    return t_list_new