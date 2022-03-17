Kodrip-lang (코랭)
==================
[엄랭](https://github.com/rycont/umjunsik-lang),
[어쩔랭](https://github.com/assertive-lang/asserlang),
[몰랭](https://github.com/ArpaAP/mollang)
등에 영향을 받은
케인 밈 기반 프로그래밍 언어다 맨이야
--------------------------------------
하더놈: [Sangchoo1201](https://github.com/sangchoo1201)  
공식 디스코드 서버: https://discord.gg/XpJYmGgSdM

# 용어

"하더놈"은 구현체를 만드는 개발자~ 를! 의미한다 맨이야.  
"돈통"은 코랭으로 코드 를! 짜는 사람을 말한다 맨이야.  
"케인인"은 컴파일러/인터프리터 를! 의미한다 맨이야.  
"방송"은 코랭으로 짜여진 모든 코드 를! 말한다 맨이야.  
"멘트"는 방송 중의 코드 한 줄 를! 말한다 맨이야.  
"이거나드셔"는 실행중 발생한 모든 에러 를! 말한다 맨이야.  
"동인천 룰"은 코랭의 문법 를! 말한다 맨이야.  

코랭의 확장자는 `.mte`다 맨이야.

# 동인천 룰 (문법)

모든 방송은, 멘트 한 줄 단위로 구분되어 실행된다 맨이야.

## 방송과 방종

모든 방송은 '안녕하세요 저는'으로 시작해서,
'죄송합니다'로 끝나야 한다 맨이야.  
만약 이를 지키지 않을 경우,
'자\~숙하자\~' 이거나드셔가 일어나고,
박벼농사가 찾아가는 수가 있어요~

## 주석 ~~유석~~

케인인님은 '코'를 싫어하시기 때문에,
'코'로 시작하는 문장은 실행 검지검지~

아래는 전부 실행되지 않는 코드다 맨이야.
```
코 케인인님 한판해요
코
```
아래는 실행되면 이거나드셔가 나는 코드다 맨이야.
```
코드립 검지검지
```

## 변수

변수를 만들거나, 대입하는 방법은 '자~'와 '를!' 을 이용하면 된다 맨이야.

```
코 변수 '케인인'을 만들고 3을 대입
자~ 케인인 를! 3

코 변수 '케인인'에 2 대입
자~ 케인인 를! 2
```

'를!' 이 없거나, '를!' 뒤에 내용이 없으면
'뭐 이런 그지 값이 다 있어?' 이거나드셔가 발생한다 맨이야.

### 변수명 규칙

키워드를 변수 이름으로 쓰는 것 검지검지~   
변수 이름이 (코랭에서 쓰이는) 기호들을 포함하는 것 검지검지~  
변수 이름이 숫자로 시작하는 것 검지검지~  

### 자료형

아직 정수형밖에 없다 맨이야.  
앞으로 다른 자료형도 추가할 예정이란다~

### 특수 변수

'코'는 늘 그렇듯이 -3000이니까 파산이야!  
'ㅖ'를 이어서 쓰면,
이어 쓴 개수만큼의 값을 가진다 맨이야.  
마찬가지로, '언'을 이어서 쓰면,
이어 쓴 개수만큼의 음수 값을 가진다 맨이야.  
'ㅖ'와 '언'을 붙여서 쓸 수는 없는게 맞아!

```
코 '감동님'에 4를 대입
자~ 감동님 를! ㅖㅖㅖㅖ

코 '케경호'에 -5를 대입
자~ 케경호 를! 언언언언언
```

### 산술 연산

산술 연산자는 '+', '-', '*', '/', '%' 죽음의 5지선다~  
사실 괄호도 쓸 수 있다 맨이야.
'/' 연산은 몫을 반환하고, '%' 연산은 나머지를 반환한다 맨이야.  

우선순위는, 괄호가 있는 것이 가장 먼저이고,
'*', '/', '%' 가 같은 우선순위,
그 다음에 '+', '-'가 처리된다 맨이야.  

### 비교 연산

비교 연산자는 '==', '!=', '<', '>', '<=', '>=' 죽음의 6지선다~  
이 정도는 돈통들도 잘 알거라고 생각해요?

## 입출력

입력은 '뽈롱'을 변수처럼 써서 받을 수 있고,
출력은 '오옹!' 키워드로 할 수 있다 맨이야.  
(아직 문자 입력/출력은 없다 맨이야)

```
코 입력받은 값에 2를 더해 출력
자~ 나이스 를! 뽈롱 + 2
오옹! 나이스
```

## 조건문

특정 조건이 참일 때 특정 코드를 실행할 수 있게 하려면,
'얘!'와 '하니?' 사이에 조건을 넣고,
'하니?' 뒤 다음 줄부터 참일 때 실행할 코드를 적은 뒤
'에이씨 나쁜 놈'으로 끝내면 된다 맨이야.  
(조건문 안에서는 들여쓰기를 하는 것을 추천한다 맨이야)

```
코 변수 '케인인'이 3이면 '케인인'에 -3을 대입
얘! 케인인 == 3 하니?
    자~ 케인인 를~ -3
에이씨 나쁜 놈
```

### else

특정 조건을 만족하지 않을 때 실행할 코드도 적으려면,
'안하니?'를 쓰면 된다 맨이야.

```
코 변수 '돈'이 1000이 넘으면 변수 '그지새끼'는 0
코 변수 '돈'이 1000이 넘지 않으면 변수 '그지새끼'는 1
얘! 돈 > 1000 하니?
    자~ 그지새끼 를! 0
안하니?
    자~ 그지새끼 를! 1
에이씨 나쁜 놈
```

## 반복문

### 횟수 반복

어떤 변수를 0부터 특정 값까지 반복하려면,
'죽이고싶은'과 '과의/와의' 사이에 대입될 변수 이름을 넣고,
'과의/와의'와 '선' 사이에 반복할 횟수를 적으면 된다 맨이야.  
마찬가지로 안쪽 코드를 끝내려면,
'에이씨 나쁜 놈'을 쓰면 된다 맨이야.

```
코 변수 '시청자'에 0부터 11 전까지 대입하며 반복
코 변수 '도네'에 0부터 10까지 더함
죽이고싶은 시청자 와의 11 선
    자~ 도네 를! 도네 + 시청자
에이씨 나쁜 놈
```

### 조건 반복

특정 조건을 만족하는 동안 코드를 반복하려면,
'인'과 '중에는!' 사이에 조건을 넣으면 된다 맨이야.  
마찬가지로 '에이씨 나쁜 놈'으로 종료할 수 있다 맨이야.

```
코 변수 '게이'가 '조이고'보다 큰 동안 게이를 1씩 감소
인 게이 > 조이고 중에는!
    자~ 게이 를! 게이 - 1
에이씨 나쁜 놈
```

## 점프문

'왔어...'를 통해서 라벨을 설정하고,
'갔어...'를 통해서 설정한 라벨로 이동한다 맨이야.  
(함수 안에서 바깥 또는 다른 함수로, 함수 밖에서 안으로 점프는 불가능하다 맨이야)  
('갔어...'를 실행하는 시점에서, 해당하는 '왔어...'가 실행되기 전이라면 이거나드셔가 발생한다 맨이야)

```
코 무한 루프를 만듦
왔어... 루프
갔어... 루프
```

## 함수

> 함수 안에 함수 안에... (쩝) 그냥 코드가 뭉탱이로 있단 말야

### 선언

위와 같은 이유로, 함수 선언은 '뭉탱이'로 시작한다 맨이야.  
함수 블럭이 끌날 때에는 '유링게슝/유리게슝'으로 끝내면 된다 맨이야.  

```
코 3을 출력하는 함수 선언
뭉탱이 출력()
    오옹! ㅖㅖㅖ
유링게슝
```

매개변수가 있을 때는, 괄호 안에 변수 이름만 넣으면 된다 맨이야.

```
코 두 입력을 더해서 출력하는 함수 선언
뭉탱이 더하기(자, 숙)
    오옹! 자 + 숙
유링게슝
```

### 리턴

함수 실행 중, '지금부터는'을 만나면 케인인님이 놀라서 함수를 탈출한다 맨이야.  
'지금부터는' 뒤에 값을 넣는 것도 가능하다 맨이야.

```
코 5를 반환하는 함수 선언
뭉탱이 반환()
    지금부터는 ㅖㅖㅖㅖㅖ
유링게슝
```

함수 내에서 어떤 상황이든, 리턴을 하지 않은 경우,
리턴 값은 자동으로 0이 된다 맨이야.

### 호출

함수 호출 방식은 다른 언어와 마찬가지다 맨이야.

```
코 입력받은 값의 2배를 반환하는 함수 선언
뭉탱이 더블(입력)
    지금부터는 입력 * 2
유링게슝

코 함수 호출
오옹! 더블(코)
코 출력: -6000
```

# 실행

(python 구현체를 기준으로 합니다.)  
터미널에서, kodrip-lang/python 위치로 이동한 뒤,
3.8 버전 이상의 python으로 main.py를 실행하면 된다 맨이야. 

실행 방법은 3가지가 있다 맨이야.  

1. `python main.py`  
이 경우에는, `main.py`와 같은 경로에 있는 `main.mte`를 실행한다 맨이야.  

2. `python main.py [방송 파일 경로]`  
이 경우에는, 해당하는 경로에 위치한 방송 파일을 실행한다 맨이야.  

3. `python main.py [방송 파일 경로] [출력 파일 경로]`  
이 경우에는, 해당하는 경로의 파일을 실행하고,
출력은 출력 파일 경로에 쓰여진다 맨이야.

파일 경로는, `main.py`에 대한 상대 경로와,
절대 경로 둘 다 가능하다 맨이야.
