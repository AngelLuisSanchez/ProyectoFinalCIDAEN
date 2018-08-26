class Celebrities():
    def __init__(self, Name, Url, Id, IdImagen):
        self.Name = Name
        self.Url = Url
        self.Id = Id
        self.IdImagen = IdImagen

    def serialize(self):
        return {
            'Name': self.Name,
            'Url': self.Url,
            'Id': self.Id,
            'IdImagen': self.IdImagen
        }
