class PostDTO:
    id = int
    password_required = bool
    tittle = str
    content = str
    author = str
    create_date = str
    like = bool
    tags = []


class CommentDTO:
    id = int
    author = str
    create_date = str
    content = str
    my_own = bool
