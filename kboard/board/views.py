from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from board.models import Post, Board, Comment
from board.forms import PostForm


def new_post(request, board_slug):
    if request.method == 'POST':
        board = Board.objects.get(slug=board_slug)
        Post.objects.create(board=board, title=request.POST['post_title_text'], content=request.POST.get('fields', ''))
        return redirect('/{}/'.format(board_slug))

    board = Board.objects.get(slug=board_slug)
    form = PostForm()
    return render(request, 'new_post.html', {'board': board, 'form': form})


def post_list(request, board_slug):
    posts_all_list = Post.objects.all()
    paginator = Paginator(posts_all_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    # page list
    page_list_count = 10
    first_page_in_list = (int((posts.number - 1) / page_list_count)) * page_list_count + 1
    end_page_in_list = (int((posts.number - 1) / page_list_count) + 1) * page_list_count
    page_list = []
    for page_num in range(first_page_in_list, end_page_in_list+1):
        if page_num > posts.paginator.num_pages:
            break
        page_list.append(page_num)

    pre_page = -1
    next_page = -1

    if posts.number > page_list_count:
        pre_page = first_page_in_list - 1

    if end_page_in_list < posts.paginator.num_pages:
        next_page = end_page_in_list + 1

    pages_info = {'pre_page': pre_page, 'page_list': page_list, 'current_num': posts.number, 'next_page': next_page}

    return render(request, 'post_list.html', {'posts': posts, 'board_id': board_slug, 'pages_info': pages_info})


def view_post(request, board_slug, post_id):
    post = Post.objects.get(id=post_id)

    return render(request, 'view_post.html', {'post': post, 'board_slug': board_slug})


def board_list(request):
    board_count = Board.objects.all().count()
    if board_count == 0:
        Board.objects.create(name='Default', slug='default')

    boards = Board.objects.all()

    return render(request, 'board_list.html', {'boards': boards})


def new_comment(request, board_slug, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        Comment.objects.create(post=post, content=request.POST['comment_content'])
        return redirect(post)


def delete_post(request, board_id, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.is_delete = True
        post.save(update_fields=['is_delete'])

        return redirect('/board/' + str(board_id) + '/')
