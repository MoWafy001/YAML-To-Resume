import pathlib

BLOCK_SIMBOL = '%block%'
VAR_SIMBOL = '$'
LIST_DICT_SIMBOL = '||'
LIST_DICT_SIMBOL_VALUE = '|+|'


class HTMLLoader:
    """
    HTML Loader for loading HTML files.
    """
    def __init__(self, html_path):
        self.html_path = html_path


    def load_html(self, file_name):
        if not file_name.endswith('.html'):
            file_name += '.html'

        with open(f"{self.html_path}/{file_name}") as f:
            html = f.read().strip()

        return html


class HTMLParser:
    """
    HTML Parser for parsing HTML content.
    """
    def __init__(self, get_var, load_html, html):
        self.get_var = get_var
        self.load_html = load_html
        self.html = html

    def parse_html(self, html=None):
        """ 
        parse the html and return it
        """

        html = html or self.html
        for method in [
                self.handle_lists_and_dicts,
                self.handle_blocks,
                self.handle_variables
        ]:
            html = method(html)

        return html

    def handle_blocks(self, html):
        blocks = html.split(BLOCK_SIMBOL)[1::2]

        for block in blocks:
            block_name, dep = self.get_block_name_and_dep(block)
            block_html = self.block_to_html(block_name, dep)
            if not block_html:
                html = html.replace(f"{BLOCK_SIMBOL}{block}{BLOCK_SIMBOL}", '')
                continue

            block_html = self.parse_html(block_html)

            html = self.symbol_to_value(html, BLOCK_SIMBOL,
                                        block, block_html)

        return html

    # find variables in lines and replace

    def handle_variables(self, html):
        vars_found = html.split(VAR_SIMBOL)[1::2]

        for var_name in vars_found:
            var_val = self.get_var(var_name)
            html = self.symbol_to_value(
                html, VAR_SIMBOL, var_name, self.get_var(var_name))

        return html

    # find list and dicts and replace

    def handle_lists_and_dicts(self, html):
        pieces = html.split(LIST_DICT_SIMBOL)

        keys_blocks = {}

        key = None
        b = None
        skip = True
        for i, v in enumerate(pieces):
            if skip:
                skip = False
                continue

            if key is None:
                key = v
                pieces[i] = ''
            else:
                b = v
                out = self.list_dict_get_out(b, key)
                pieces[i] = out
                skip = True
                key = None

        return ' '.join(pieces)

    def loop_over_list_or_dict(self, var, b, key):
        out = ""
        if type(var) is list:
            out = self.handle_list(out, var, b, key)
        else:  # dict
            out = self.handle_dict(out, var, b, key)

        return out

    """
    Helper Methods
    """

    def get_block_name_and_dep(self, block):
        block_l = block.split('?')
        block_name = block_l[0].strip()
        dep = None

        if len(block_l) == 2:
            dep = block_l[1]
            if dep.strip() == '':
                dep = block_name

        return block_name, dep

    def block_to_html(self, block_name, dep):
        """ 
        If a block has a dependency, check if the dependency exists.
        If it does, return the block HTML.
        If it doesn't, return an empty string.
        If a block doesn't have a dependency, return the block HTML.
        """

        if not dep:
            return self.load_html(block_name)

        try:
            self.get_var(dep)  # check if the dependency exists
            return self.load_html(block_name)
        except:
            return ''

    def symbol_to_value(self, line, symbol, var, value):
        return line.replace(f"{symbol}{var}{symbol}", value)

    def list_dict_get_out(self, b, key):
        try:
            listordict = self.get_var(key)
            return self.loop_over_list_or_dict(listordict, b, key)
        except:
            return ''

    def handle_list(self, out, var, b, key):
        for val in var:
            if type(val) is str:
                nb = self.symbol_to_value(b, LIST_DICT_SIMBOL_VALUE,
                                          key+"_val", val.replace('\n', '<br>'))
                out += nb
            else:
                out += self.loop_over_list_or_dict(val, b, key)
        return out

    def handle_dict(self, out, var, b, key):
        for k in var:
            nb = self.symbol_to_value(b, LIST_DICT_SIMBOL_VALUE,
                                      key+"_key", k.replace('\n', '<br>'))
            if type(var[k]) == list:
                out += self.handle_list_in_dict(var[k], nb, key)

            else:
                nb = self.symbol_to_value(nb, LIST_DICT_SIMBOL_VALUE,
                                          f"{key}_val", var[k].replace('\n', '<br>'))
                out += nb

        return out

    def handle_list_in_dict(self, var_k, nb, key):
        c = 0
        for i in var_k:
            nb = self.symbol_to_value(nb, LIST_DICT_SIMBOL_VALUE,
                                      f"{key}_val_{c}", i.replace('\n', '<br>'))
            c += 1

        return nb


class TemplateEngine:
    """
    Template Engine for rendering HTML templates with variables.
    """
    def __init__(self, base_file_path, get_var):
        # to get variables
        self.get_var = get_var

        # base HTML file path
        self.base_file_path = base_file_path
        self.base_file_name = pathlib.Path(base_file_path).name

        # the path of the directory where the HTML files are
        self.html_path = str(pathlib.Path(base_file_path).parent)

        # HTML Loader
        html_loader = HTMLLoader(self.html_path)
        self.load_html = html_loader.load_html

        # get the HTML of the base HTML file
        self.html = self.load_html(self.base_file_name)

        # HTML Parser
        html_parser = HTMLParser(self.get_var, self.load_html, self.html)
        self.parse_html = html_parser.parse_html


    # render
    def render(self):
        job_title = self.get_var('job title').strip().replace(' ', '_')
        full_name = self.get_var('full name').strip().replace(' ', '_')
        
        file_name = f"{full_name}_{job_title}"

        return self.parse_html(), file_name