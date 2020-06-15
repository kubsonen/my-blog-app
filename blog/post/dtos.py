
class PostDTO:
    id = int
    password_required = bool
    tittle = str
    content = str
    author = str
    create_date = str
    like = bool
    unlock = bool
    tags = []
    miniature = str
    mainImage = str


class CommentDTO:
    id = int
    author = str
    create_date = str
    content = str
    my_own = bool
