class Celebrities():
    def __init__(self, Id, Name, Url, IdImagen):
        self.Id = Id
        self.Name = Name
        self.Url = Url
        self.IdImagen = IdImagen

    def serialize(self):
        return {
            'Id': self.Id,
            'Name': self.Name,
            'Url': self.Url,
            'IdImagen': self.IdImagen
        }
