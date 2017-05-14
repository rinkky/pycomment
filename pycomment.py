# coding=utf-8

import sublime
import sublime_plugin

class PycommentCommand(sublime_plugin.TextCommand):
    def run (self, edit):
        """run the command
        
        Args:
          edit -- sublime.Edit. used by insert()/erase()/replace()
        Returns: 
        Raises: 
        """

        pt = self.view.sel()[0].a

        rgs = self.view.find_by_selector(
            "meta.function.python, "
            "meta.function.parameters.python, "
            "meta.function.parameters.default-value.python, "
            "punctuation.section.function.begin.python"
        )
        if not rgs:
            return
        rg = self.get_near_fun(rgs, pt)

        rgs_args = self.view.find_by_selector("variable.parameter.python")
        rgs_args = self.get_all_contain(rg, rgs_args)
        args = [self.view.substr(x) for x in rgs_args]

        ptdef = self.view.find_by_class(rg.a-1, True, sublime.CLASS_WORD_START)
        tab_size = self.view.settings().get("tab_size")
        begin = tab_size + ptdef - rg.a
        
        tmp = [(begin+2)*" "+ arg + " -- \n" for arg in args if arg != "self"]
        comment_args = (
            "{0}Args:\n".format(begin * " ")
            +"".join(tmp)
        ) if args else ""
        
        comment = (
            "\n{0}\"\"\"\n"
            "{0}\n"
            + comment_args +
            "{0}Returns: \n"
            "{0}Raises: \n"
            "{0}\"\"\"\n"
        ).format(" " * begin)
        print(comment)
        self.view.insert(edit, rg.b, comment)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(rg.b+begin+4, rg.b+begin+4))

    @staticmethod
    def get_all_contain(rg, rgs):
        """from rgs get all regions that contained by rg.
        
        Args:
          rg -- type: sublime.Region
          rgs -- type: sublime.Region
        Returns: a list of Region
        Raises: 
        """

        lst = []
        for x in rgs:
            if rg.contains(x):
                lst.append(x)
        return lst

    @staticmethod
    def get_near_fun(rgs, pt):
        """from rgs get the region near by pt
        
        Args:
          rgs -- a list of sublime.Region
          pt -- type: int. the offset from the beggnning.
        Returns: type: sublime.Region
        Raises: 
        """

        distances = [pt-rg.a for rg in rgs if pt >= rg.a]
        m = min(distances)
        return rgs[distances.index(m)]
