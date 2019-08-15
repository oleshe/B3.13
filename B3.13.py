class HTML:
    """
    2. Класс HTML определяет, куда сохранять вывод: на экран через print или в файл.
    """
    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        opening = "<html>\n"
        internal = ""
        for child in self.children:
            internal += str(child)
        ending = "</html>"

        if self.output is None :
            print(opening + internal + ending)
            return None
        else :
            with open(self.output, "w") as OutFile :
                OutFile.write(opening + internal + ending)
            return None

class TopLevelTag(HTML):
    """
    3. Объекты класса TopLevelTag скорее всего не содержат внутреннего текста и всегда парные.
        Наследование от HTML сделанно для использование метода __iadd__
    """
    def __init__(self, tag):
        self.tag = tag
        self.children = []

    def __str__(self):
        opening = "<{tag}>\n".format(tag=self.tag)
        internal = ""
        for child in self.children:
            internal += str(child)
        ending = "</%s>\n" % self.tag
        return opening + internal + ending

    def __exit__(self, type, value, traceback):
        pass

class Tag(TopLevelTag):
    """
    4. Объекта класса Tag могут быть непарные или быть парные и содержать текст внутри себя.
    5. Должна быть возможность задать атрибуты в Tag, но в данном задании для TopLevelTag это необязательное условие.
    """
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.text = ""
        self.children = []
        self.attributes = {}
        if klass is not None:
            self.attributes["class"] = " ".join(klass)
        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value            

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if attrs : attrs = " " + attrs

        if self.children:
            opening = "<{tag}{attrs}>\n".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "</%s>\n" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag}{attrs}/>\n".format(tag=self.tag, attrs=attrs)

            else:
                return "<{tag}{attrs}>{text}</{tag}>\n".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )

if __name__ == "__main__":
    with HTML(output=None) as doc: #output="index.html"
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body
