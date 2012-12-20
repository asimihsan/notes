# Your function should display HTML according to a given parse tree.

# graphics.warning(msg) displays an error message. Upon encountering mismatched
# tags, use graphics.warning to display the error message: "mismatched tag".

# To display a tag, use graphics.begintag(tag,args) at the start and
# graphics.endtag() at the end of the tag.

import graphics

def interpret(trees): # Hello, friend
    for tree in trees: # Hello,
        # ("word-element","Hello")
        nodetype=tree[0] # "word-element"
        if nodetype == "word-element":
            graphics.word(tree[1])
        elif nodetype == "tag-element":
            # <b>Strong text</b>
            tagname = tree[1] # b
            tagargs = tree[2] # []
            subtrees = tree[3] # ...Strong Text!...
            closetagname = tree[4] # b
            # QUIZ: (1) check that the tags match
            # if not use graphics.warning()
            if tagname != closetagname:
                graphics.warning("Mismatched tag. start: '%s', end: '%s'" % (tagname, closetagname))
            else:
                #  (2): Interpret the subtree
                # HINT: Call interpret recursively
                graphics.begintag(tagname, {})
                interpret(subtrees)
                graphics.endtag()

# Note that graphics.initialize and finalize will only work surrounding a call
# to interpret

graphics.initialize() # Enables display of output.

tree = [('tag-element', 'body', [],
            [('tag-element', 'b', [],
                [('word-element', 'Hello World')],
            'b')],
        'body')]

interpret(tree)
graphics.finalize() # Enables display of output.


