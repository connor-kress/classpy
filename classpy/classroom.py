class ClassRoom:
    def __init__(self, name: str, url: str) -> None:
        assert isinstance(name, str)
        assert isinstance(url, str)
        self.name = name
        self.url = url
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}', '{self.url}')"
