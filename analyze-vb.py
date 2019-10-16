import sys
import re

LITERAL_CHAR = '"'
WHITESPACE_CHAR = " "
COMMENT_CHAR = "'"
LINEFEED_CHAR = "\n"


# remove comment from string
def remove_comment(text):
    rtn = ""
    in_comment = False
    in_literal = False
    for c in text:
        if c == LITERAL_CHAR:
            if not in_literal:
                in_literal = True
            else:
                in_literal = False

        if c == COMMENT_CHAR:
            if not in_literal:
                in_comment = True

        if c == LINEFEED_CHAR:
            rtn += c
            in_comment = False
            in_literal = False
        elif in_comment:
            rtn += WHITESPACE_CHAR
        else:
            rtn += c
    return rtn


def impl_to_referenced_objects(this_classname, impl):
    rtn = []
    referenced_objects = {}
    referenced_functions = []
    referenced_procedures = []
    # collect referenced_objects
    text = impl
    while True:
        match = re.search(r"Dim ([a-zA-Z0-9_]+) As ([a-zA-Z0-9_]+)", text, re.MULTILINE | re.DOTALL)
        if match:
            variable = match.group(1)
            classname = match.group(2)
            # print("variable:{}, classname:{}".format(variable, classname))
            referenced_objects[variable] = classname
            text = text[match.end(0):]
        else:
            break

    text = impl
    while True:
        match = re.search(r"\s+([a-zA-Z0-9_]+)\s*\(", text, re.MULTILINE | re.DOTALL)
        if match:
            function = match.group(1)
            referenced_functions.append(function)
            text = text[match.end(0):]
        else:
            break

    text = impl
    while True:
        match = re.search(r"\s+.+\.StoredProcedure = \"([a-zA-Z0-9_]+)\"", text, re.MULTILINE | re.DOTALL)
        if match:
            procedure = match.group(1)
            referenced_procedures.append(procedure)
            text = text[match.end(0):]
        else:
            break

    # parse referer
    for var in referenced_objects.keys():
        text = impl
        while True:
            match = re.search(r"\s+{}\.([a-zA-Z0-9_]+).*\n".format(var), text, re.MULTILINE | re.DOTALL)
            if match:
                rtn.append(referenced_objects[var] + "." + match.group(1))
                text = text[match.end(0):]
            else:
                break
    for f in referenced_functions:
        rtn.append(this_classname + "." + f)

    for p in referenced_procedures:
        rtn.append(p)

    return rtn


def extract_methods(class_name, text):
    methods = {}
    while True:
        #result = re.findall("((Public|Private|Protected) (Sub|Function) ([^\n]+)\n(.*)End (Sub|Function)\n+)*$", text,
        match = re.search(r"(Public|Private|Protected) (Sub|Function) ([^\(]+)", text, re.MULTILINE | re.DOTALL)
        if match:
            # print("{} {} {}".format(match.group(1), match.group(2), match.group(0)))
            method_name = match.group(3)
            # print("method={}".format(match.group(3)))
            text = text[match.end(0):]
            match = re.search(r"End (Sub|Function)\n", text, re.MULTILINE | re.DOTALL)
            if match:
                # method_impl = text[0:match.start(0)]
                referenced_objects = impl_to_referenced_objects(class_name, text[0:match.start(0)])
                methods[method_name] = referenced_objects
                # print("method impl={},{}".format(match.pos, match.endpos))
                text = text[match.end(0):]
        else:
            break

        # text = result.group(4)
        # result = re.search("End (Sub|Function)(.*)$", text, re.MULTILINE | re.DOTALL)
        # print("pos={}".format(result.pos))
        # if result:
        #     method_impl = result.group(1)
        #     methods[method_name] = method_impl
        #     text = result.group(2)
        # else:
        #     print("no method delimiter")
        #     break
    return methods


def extract_class(text):
    result = re.search(r"(Partial )*Public Class ([^\n]*)\n(.*)End Class\n(\s*\n*)*$", text, re.MULTILINE | re.DOTALL)
    if result:
        # print("match")
        class_name = result.group(2)
        class_impl = result.group(3)
        methods = extract_methods(class_name, class_impl)
        return class_name, methods
    else:
        # print("unmatch")
        return None


def extract_import_modules(text):
    result = re.finditer(r"Imports ([a-zA-Z\.]+)", text, re.MULTILINE | re.DOTALL)
#    for m in result:
#        print(m.group(1))
    return


def read_file_content(filename):
    try:
        with open(filename, "r") as f:
            text = f.read()
            return text
    except Exception as e:
        print(e.args)
        exit(-1)


if __name__ == "__main__":
    # if len(sys.argv) == 1:
    #     print("Error: too few argument")
    #     exit(-1)
    #
    # vbfile = sys.argv[1]
    vbfile = "Test.vb"
    text = read_file_content(vbfile)
    text = remove_comment(text)
    class_name, class_methods = extract_class(text)
    extract_import_modules(text)
    # print("class name:{}".format(class_name))
    # print("class methods:")
    # print(class_methods)
    for k in class_methods.keys():
        for m in class_methods[k]:
            print("{}.{},{}".format(class_name, k, m))
