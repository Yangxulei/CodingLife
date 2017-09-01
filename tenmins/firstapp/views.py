from django.shortcuts import render, redirect,HttpResponse
from firstapp.models import Article,Tickets, Comment_New, UserProfile
from firstapp.forms import CommentForm, ArticleForm, ProfileForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth import login as auth_login , authenticate ,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

def index(request,cate=None):
    context = {}
    if cate == None:
        result_list = Article.objects.order_by('-createtime')
    if cate == 'hot':
        result_list = Article.objects.filter(cate_choice='hot').order_by('-createtime')
    if cate == 'best':
        result_list = Article.objects.filter(cate_choice='best').order_by('-createtime')


    page_robot = Paginator(result_list, 9)
    page_num = request.GET.get('page')

    try:
        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger :
        article_list = page_robot.page(1)

    print (article_list.number)


    # 传递页码
    if article_list.number <= 3:
        index_list = [1,2,3,'...',page_robot.num_pages]

    elif article_list.number < page_robot.num_pages -2 :
        index_list = [article_list.number-2, article_list.number-1, article_list.number, '...',page_robot.num_pages]

    elif article_list.number == page_robot.num_pages -2 :
        index_list = [article_list.number-2, article_list.number-1, article_list.number, page_robot.num_pages-1, page_robot.num_pages]

    elif article_list.number == page_robot.num_pages - 1:
        index_list = [article_list.number-3,article_list.number-2,article_list.number-1,article_list.number,page_robot.num_pages]

    elif article_list.number == page_robot.num_pages:
        index_list = [page_robot.num_pages-x for x in range(4,-1,-1)]


    # 是否修改过头像、资料
    try:
        my_profile = request.user.userprofle
    except ObjectDoesNotExist and AttributeError:
        my_profile = None

    context = {}
    context['index_list'] = index_list
    context["article_list"] = article_list
    context['my_profile'] = my_profile
    return render(request, 'index.html', context)


def detail(request, page_num, error_form=None):

    context = {}

    if error_form == None:
        form = CommentForm()

    if error_form :
        form = error_form

    article = Article.objects.get(id=page_num)
    # 更新文章浏览量
    article.views = article.views + 1
    article.save()
    context['view_count'] = article.views
    # 获取关联这篇文章的所有评论
    comments = Comment_New.objects.filter(belong_to_id=article.id)

    # 处理投票业务的数据渲染
    all_ticket_count = article.tickers.count()
    ticket_like_count = article.tickers.filter(vote='like').count()
    ticket_dislike_count = article.tickers.filter(vote='dislike').count()
    context['all_ticket_count'] = all_ticket_count
    context['ticket_like_count'] = ticket_like_count
    context['ticket_dislike_count'] = ticket_dislike_count

    if request.user.is_authenticated:
        user_vote_ticket_like = article.tickers.filter(voter_id=request.user.id,vote='like').count()
        user_vote_ticket_dislike = article.tickers.filter(voter_id=request.user.id,vote='dislike').count()
        context['user_vote_ticket_like'] = user_vote_ticket_like
        context['user_vote_ticket_dislike'] = user_vote_ticket_dislike


    context['article'] = article
    context['form'] = form
    context['comments'] = comments
    return render(request, 'detail.html', context)


def detail_vote(request, id):
    if request.user.is_authenticated:
        vote = request.POST['vote']
        article = Article.objects.get(id=id)
        user = User.objects.get(username=request.user.username)
        ticket = Tickets(voter=user,article=article,vote=vote)
        ticket.save()
        return redirect('detail',id)
    else:
        return redirect('register')

# 新的评论功能 用户可以对一篇文章点评多次
def detail_comment(request, page_num):
    # 判断是否登录
    if request.user.is_authenticated:
        # 表单绑定
        form = CommentForm(request.POST)
        # 验证表单
        if form.is_valid():
            content = form.cleaned_data['comment']
            publisher = request.user
            belong_to = Article.objects.get(id=page_num)

            comment =  Comment_New(publisher=publisher, content=content, belong_to=belong_to)
            comment.save()
            return redirect('detail',page_num)
        else:
            return detail(request, page_num=page_num, error_form=form)


# 注册业务
def register(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            auth_login(request, user)
            return redirect('index')
    context['form']= form
    return render(request, 'register.html', context)

# 登录业务
def login(request):
    context = {}
    if request.method == 'GET':
        form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            print ('已经登录')
            return redirect('index')
    context['form']= form
    return render(request, 'register.html', context)


# 发布文章
def publish_get(request,error_form=None):
    context = {}

    if error_form != None:
        form = error_form
        print ([field for field in form])
    else:
        form = ArticleForm()

    context['form'] = form
    return render(request, 'publish.html', context)

# 发布-POST
def publish_post(request):
    form = ArticleForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']
        imgURL = form.cleaned_data['imgURL']
        content = form.cleaned_data['content']
        choice = form.cleaned_data['category']
        user = request.user
        article = Article(title=title, img=imgURL, content=content,cate_choice=choice,author=user)
        article.save()
        page_id = article.id
        return redirect('detail',page_id)

    else:
        return publish_get(request,form)


# search
def search(request):
    context = {}
    index_list = []

    if request.GET.get('name') == None:
        print ('name is None')
        return render(request, 'search.html')
    if request.GET.get('name')!= None and request.GET.get('cate') == None or request.GET.get('cate') == 'all':
        # 这种情况就是在搜索all类型
        name = request.GET.get('name')
        query_set = Article.objects.filter(title__contains=name)
        context['name'] = name
        context['cate'] = 'all'

    if request.GET.get('cate') == 'hot' or request.GET.get('cate') == 'best':
        # 在搜索hot或者best类型
        name = request.GET.get('name')
        choice = request.GET.get('cate')
        query_set = Article.objects.filter(title__contains=name,cate_choice=choice)
        context['name'] = name
        context['cate'] = choice

    # 判断query_set是否有效，返回合适的article_list
    if query_set.count() > 0:
        # 如果有效，生成分页器，找出所请求的页面数据
        page_robot = Paginator(query_set,9)
        page_num = request.GET.get('page')
        try :
            article_list = page_robot.page(page_num)
        except PageNotAnInteger :
            article_list = page_robot.page(1)
        except EmptyPage :
            article_list = page_robot.page(page_robot.num_pages)
    else:
        article_list = None
    # 放入上下文
    context['article_list'] = article_list

    # 如果article_list = None
    if article_list == None:
        index_list = None
    else:
        # 传递页码
        # 1. 判断搜索结果是否小于5页
        if page_robot.num_pages <=5:
            # 构造页码数组
            index_list = [x for x in range(1,(page_robot.num_pages + 1))]
        else:
            # 2. 如果当前页码数<=3
            if article_list.number <= 3:
                index_list = [1,2,3,'...',page_robot.num_pages]
            elif article_list.number < page_robot.num_pages -2:
                index_list = [article_list.number-2, article_list.number-1, article_list.number, '...', page_robot.num_pages]
            elif article_list.number == page_robot.num_pages-2:
                index_list = [article_list.number-2, article_list.number-2, article_list.number, page_robot.num_pages-1, page_robot.num_pages]
            else:
                index_list = [(page_robot.num_pages - x) for x in range(4,-1,-1)]

    # 将页码放入上下文
    context['index_list'] = index_list
    return render(request, 'search.html', context)


# 个人中心
@login_required
def user_profile(request,error_form=None,error_password_form=None):
    context = {}
    index_list = []
    # 检查是否更新过个人资料
    try:
        new_profile = request.user.userprofle
    except ObjectDoesNotExist:
        new_profile = None

    context['new_profile'] = new_profile
    # 渲染密码表单
    password_form = PasswordChangeForm(request.user)
    context['password_form'] = password_form

    # 获取点赞的数据
    user_like_tickets_count = request.user.tickers.filter(vote='like').count()
    print (user_like_tickets_count)



    # 判断是否有点赞的数据
    if user_like_tickets_count > 0:
        context['fav_articles'] = True
        all_tickets = request.user.tickers.all()
        # 构造分页器
        page_robot = Paginator(all_tickets,3)
        page_num = request.GET.get('page')
        # 获取当页请求的数据
        try:
            result = page_robot.page(page_num)
        except EmptyPage:
            result = page_robot.page(page_robot.num_pages)
        except PageNotAnInteger:
            result = page_robot.page(1)

        context['result'] = result
        # 传递页码
        if page_robot.num_pages <=5:
            # 构造页码数组
            index_list = [x for x in range(1,(page_robot.num_pages + 1))]
        else:
            # 2. 如果当前页码数<=3
            if result.number <= 3:
                index_list = [1,2,3,'...',page_robot.num_pages]
            elif result.number < page_robot.num_pages -2:
                index_list = [result.number-2, result.number-1, result.number, '...', page_robot.num_pages]
            elif result.number == page_robot.num_pages-2:
                index_list = [result.number-2, result.number-2, result.number, page_robot.num_pages-1, page_robot.num_pages]
            else:
                index_list = [(page_robot.num_pages - x) for x in range(4,-1,-1)]
        context['index_list'] = index_list

    else:
        context['fav_articles'] = False

    print (index_list)

    # 处理修改个人资料的表单业务
    if error_form == None:
        if request.GET.get('cate') == None:
            form = ProfileForm()
            context['form'] = form
            return render(request,'myinfo.html',context)
        else:
            cate = request.GET.get('cate')
            context['cate']=cate
            form = ProfileForm()
            context['form'] = form
            return render(request, 'myinfo.html',context)
    else:
        context['form'] = error_form
        return render(request, 'myinfo.html',context)

@login_required
def setprofile(request):
    form = ProfileForm(request.POST,request.FILES)
    if form.is_valid():
        # 判断是否更改过个人资料
        try:
            # 创建过的话，就直接更新
            my_profile = request.user.userprofle
            my_profile.avatar = request.FILES['avatar']
            my_profile.nickname = form.cleaned_data['name']
            my_profile.gender = form.cleaned_data['sexy']
            my_profile.save()
        except ObjectDoesNotExist:
            # 如果没有创建，就创建一个新的userprofile对象
            image = request.FILES['avatar']
            name = form.cleaned_data['name']
            sexy = form.cleaned_data['sexy']
            userprofile = UserProfile(avatar=image,belong_to=request.user,gender=sexy,nickname=name)
            userprofile.save()
        return redirect('user_profile')
    else:
        return user_profile(request,form)

# 修改密码
@login_required
def password_change(request):
    context={}
    # 绑定表单
    form = PasswordChangeForm(request.user,request.POST)
    # 判断是否有效
    if form.is_valid():
        user = form.save()
        # 更新浏览器session
        update_session_auth_hash(request,user)
        return HttpResponse('<h3>密码修改成功</h3>')
    else:
        error = form.errors
        return HttpResponse('<h3>密码修改失败</h3>%s'%error)
