def config_section_map(self, section):
    dict1 = {}
    options = self.options(section)
    for option in options:
        try:
            dict1[option] = self.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
