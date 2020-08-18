# 동영상을 올릴수있는 웹사이트

<img width="100%" alt="대시보드" src="readmeImg\메인사진.png">

>'isutube'는 여러 사용자들이 본인이 좋아하는 가수의 라이브 영상을 올려서 서로 댓글을 공유하고 본인이 마음에 드는 영상에 좋아요도 추가할 수 있는 웹사이트입니다

## 필요기능
- classView를 이용한 간단하고 빠른 웹사이트 CRUD 구성
- 자체 LoginView, LogoutView를 이용해 로그인 관리 
- 검색폼을 통해 검색단어를 가져와 query_set을 filtering하여 새로운 list를 보여주기
- page_obj 객체를 이용해서 paging 기능 구현
- profile페이지를 만들어 자기가 올린 영상들 나열하기
- detailView에서 각 영상마다 댓글폼/댓글리스트 구현하기
- 각 Video마다 query_set을 가져올때마다 view_count 컬럼을 하나씩추가해서 조회수 구현하기
- Video테이블의 like컬럼과 장고 User를 다대다 매칭하여 좋아요 기능 구현


## 검색폼 구현
listView는 페이지에 request를 보내줄때마다 db에서 list를 불러와서 뿌려주는데 만약에 검색폼에 검색내용이 GET방식으로 전달된다면 새로운 쿼리셋을 불러와 뿌려주는 방식으로 구현했습니다
<img width="100%" alt="대시보드" src="readmeImg\list뷰.png">
ListView는 실행될때마다 get_queryset으로 model에 지정된 모델을 기준으로 모든 자료를 가져오는데(Model.objects.all()과 동일) GET프로토콜로 지정된 자료가 'q'라는 이름으로 넘어온다면 filter함수를 이용해서 title에 해당 내용이 있는 자료만 리턴해줌으로 검색기능을 구현했습니다


## 댓글 구현
<img width="100%" alt="대시보드" src="readmeImg\댓글.png">
User와 Video 둘을 참조키로 가지고 있으며 CreateView를 상속받아 사용했습니다. 각 댓글은 request의 User를 분석해서 삭제버튼을 다르게 랜더링하여서 본인이 쓴 댓글만 삭제가 가능합니다  

<img width="100%" alt="대시보드" src="readmeImg\video모델.png">
댓글 기능 구현후에 제일 최신 댓글이 제일 위로 와서 먼저 보이게 하고싶었습니다.  

view단에서 따로 무언가를 한게 아니고 템플릿으로 넘어와서 각 Video객체에서 자식_set에 접근하는 방식으로 반복문을 돌렸기때문에 Jinja문법으로 order_by를 하려고 했지만 Jinja안에서는 먹히지 않았고 구글검색을 통해 Jinja 필터중에 sort() 함수가 있다는걸 발견했고 {% for comment in video.comment_set.all.sort(reverse=True) %} 같은 방식으로 해보았고 약간의 변형을 계속 줘보았지만 먹히지않았고 view단에서 get_queryset을 오버라이딩하거나 함수형 view로 만들려고 했습니다  

그러다가 Model에서 Mata 클래스설정이 생각났고 ordering = ['-id']로 생성된 역순으로 댓글을 나열해 구현할수 있었습니다

## 좋아요 구현
<img width="100%" alt="대시보드" src="readmeImg\likeUpdate뷰.png">

각 User는 여러Video에 좋아요를 누를수있고 여러 Video또한 각 User에게 좋아요를 받을수 있기때문에 Video와 User를 다:다 매칭해서 db를 구성했습니다  
처음 생각은 javascript를 사용해서 좋아요 updateView로 넘기려고 했으나 post요청을 하려면 db자료를 restAPI로 받아야 할거같은 생각이 들어 form으로 정보를 넘겨야겠다고 생각해서 form으로 좋아요버튼을 구현하다가 굳이 지금 좋아요상태를 넘기는것보다 view단에서 현재유저가 Video의 'like'컬럼에 있는지 확인해서 분기한다음 객체를 remove/add하는게 낫다는 판단이 들어서 view를 위와 같이 수정했습니다
<img width="100%" alt="대시보드" src="readmeImg\좋아요html.png">
html단에서 마찬가지방법으로 분기하여 서로다른 색깔의 하트아이콘을 배치하였습니다

## 디자인
django-bootstrap4와 fontawsome을 이용하여 빠른개발에 이용했습니다

## 헤맸던부분/보완할점
페이징구현을 처음부터 bootstrap을 사용해서 만들었기때문에 구체적으로 page_obj의 어떤 부분이 페이징을 구성하는지 이해못해서 document를 보고 함수형view에서 페이징을 구현해본후에 이해 할수 있었습니다  

지금 좋아요 버튼을 누를때마다/댓글을 쓸때마다 새로 page가 갱신되고 보고있던 영상도 끊겨서 처음부터 다시 재생됩니다. React의 state상태 관리를 통해서 fetch통신으로 좋아요 버튼을 구현할 예정입니다
