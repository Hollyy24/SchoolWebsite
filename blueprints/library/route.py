from flask import Blueprint, render_template, session, flash, redirect, url_for,request
from flask_login import current_user, login_required
from blueprints.register.models import SearchBook, Library,AddBook, db

library = Blueprint("library", __name__, template_folder="templates")


@library.route("/",methods=["POST","GET"])
def index():
    searchbook = SearchBook()
    if searchbook.validate_on_submit():
        way = searchbook.ways.data
        content = searchbook.content.data
        if way == "書名":
            books = Library.query.filter_by(book_title=content).all()
        elif way == "作者":
            books = Library.query.filter_by(author=content).all()
        elif way == "編號":
            books = Library.query.filter_by(id=content).all()
        elif way == "ISBN碼":
            books = Library.query.filter_by(ISBN_number=content).all()
    else:
        page = request.args.get("page",1,type=int)
        books = Library.query.filter_by().paginate(page=page,per_page=10,error_out=False)
    return render_template("library.html", books=books, searchbook=searchbook,current_page=books.page,
                           total_pages=books.pages)


@library.route("/delete/<string:book_id>", methods=["POST","GET"])
@login_required
def delete(book_id):
    book = Library.query.filter_by(id=book_id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        flash("刪除成功")
    else:
        flash("無法刪除")
    return redirect(url_for("library.index"))


@library.route("/edit/<string:book_id>", methods=["POST","GET"])
@login_required
def edit(book_id):
    book = Library.query.filter_by(id=book_id).first()
    bookform = AddBook(id=book.id,book_title=book.book_title,
                       author = book.author,ISBN_number=book.ISBN_number)
    if bookform.validate_on_submit():
        book.id = bookform.id.data
        book.book_title = bookform.book_title.data
        book.author = bookform.author.data
        book.ISBN_number = bookform.ISBN_number.data
        db.session.commit()
        flash("修改成功")
        return redirect(url_for("library.index"))
    return render_template("book_edit.html",book=book,bookform=bookform)