from django.http import HttpResponse
from .models import ArticlePost
# 引入redirect 重定向模块
from django.shortcuts import render, redirect
# 引入表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from comment.models import Comment
from .models import ArticleColumn
from comment.forms import CommentForm
from taggit.models import Tag

import markdown


# # 文章列表
# def article_list(request):
#     # 取出所有文章
#     search = request.GET.get('search')
#     order = request.GET.get('order')
#     if search:
#         if order == 'total_views':
#             # 用 Q对象 进行联合搜索
#             article_list = ArticlePost.objects.filter(
#                 Q(title__icontains=search) |
#                 Q(body__icontains=search)
#             ).order_by('-total_views')
#         else:
#             article_list = ArticlePost.objects.filter(
#                 Q(title__icontains=search) |
#                 Q(body__icontains=search)
#             )
#     else:
#         # 将 search 参数重置为空
#         search = ''
#         if order == 'total_views':
#             article_list = ArticlePost.objects.all().order_by('-total_views')
#         else:
#             article_list = ArticlePost.objects.all()
#     # 每页显示1篇文章
#     paginator = Paginator(article_list, 10)
#     # 获取 url 中的页码
#     page = request.GET.get('page')
#     # 将导航对象相应的页码返回给 articles
#     articles = paginator.get_page(page)
#     # 引入评论表单
#     comment_form = CommentForm()
#     #print("yes")
#     # 需要传递给模板的对象
#     tags = Tag.objects.all()
#
#     #print(tags)
#     context = {'articles': articles, 'order': order, 'search': search, 'comment_form': comment_form, 'tags': tags, }
#     # render 函数：载入模板，返回context对象
#     return render(request, 'article/list.html', context)

# 文章详情
def article_detail(request,id):
    # 取出相应文章
    article = ArticlePost.objects.get(id=id)
    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    # 将markdown语法渲染成html样式
    article.total_views += 1
    article.save(update_fields=['total_views'])
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    comment_form = CommentForm()
    # 需要传递给模板的对象
    context = { 'article': article, 'toc': md.toc, 'comments': comments, 'comment_form': comment_form, }
    # 载入模板，返回context对象
    return render(request, 'article/detail.html', context)

# 写文章的视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 增加 request.FILES
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交数据是否满足模型要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不要提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果进行过删除用户表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)

            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 将文章保存到数据库中
            new_article.save()
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
        return render(request,'article/create.html',context)

# 删除文章
def article_delete(request,id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用.delete() 方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")

# 安全删除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request,id):

    if request.method=='POST':
        article=ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("抱歉，你无权修改这篇文章。")
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request,id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新title、body等字段
    GET方法进入初始表单页面
    """
    # 获取要修改的文章对象
    article = ArticlePost.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            # 保存新写入的 title、body数据并保存
            article.title=request.POST['title']
            article.body=request.POST['body']
            article.save()
            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("表单信息有误，请重新填写。")

    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
        }
        return render(request,'article/update.html',context)

def article_list(request):
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    tags = Tag.objects.all()
    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
        'tags': tags,
    }

    return render(request, 'article/list.html', context)











