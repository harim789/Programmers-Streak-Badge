<div align="center">

# Programmers Streak Badge

**프로그래머스 점수 · 랭킹 · 해결한 문제 수**와 **매일 연속으로 푼 기록**을<br>
GitHub 프로필에 보여주는 배지입니다.

<img src="docs/preview.png" alt="Programmers Streak Badge 미리보기" width="100%">

</div>

<br>

## 목차

1. [무엇을 보여주나요?](#-무엇을-보여주나요)
2. [이 문서 보는 법](#-이-문서-보는-법)
3. [준비물](#-준비물)
4. [설치하기 (약 10분)](#-설치하기-약-10분)
   - [1단계. 백준허브 설치](#1단계-백준허브-설치)
   - [2단계. 이 템플릿으로 내 저장소 만들기](#2단계-이-템플릿으로-내-저장소-만들기)
   - [3단계. 백준허브 저장소 읽기 토큰 만들기 (비공개일 때만)](#3단계-백준허브-저장소-읽기-토큰-만들기-비공개일-때만)
   - [4단계. 비밀값 등록하기](#4단계-비밀값-등록하기)
   - [5단계. 저장소 이름 알려주기](#5단계-저장소-이름-알려주기)
   - [6단계. 첫 실행](#6단계-첫-실행)
   - [7단계. 프로필 README에 붙이기](#7단계-프로필-readme에-붙이기)
5. [(선택) 풀자마자 바로 갱신하기](#-선택-풀자마자-바로-갱신하기)
6. [배지 읽는 법](#-배지-읽는-법)
7. [자주 묻는 질문](#-자주-묻는-질문)
8. [보안 안내](#-보안-안내)
9. [크레딧](#-크레딧)

<br>

## 🟣 무엇을 보여주나요?

| 위치 | 내용 |
|---|---|
| **왼쪽 Stats** | 프로그래머스 **점수**, **랭킹**, **해결한 문제 수** |
| **오른쪽 위** | **현재 연속 풀이 일수**, **최장 기록**, 오늘 풀었는지 여부 |
| **오른쪽 잔디** | 최근 16주 동안 날마다 푼 문제 수. **안 푼 날은 주황 테두리**로 따로 표시 |

- 매시간 자동으로 갱신됩니다. (선택 설정을 하면 문제를 풀자마자 갱신)
- 날짜는 **한국 시간(KST)** 기준입니다. 오늘 아직 안 풀었어도 **자정 전까지는 연속 기록이 끊기지 않고**, 대신 모래시계와 함께 `NOT YET TODAY`가 표시됩니다.

<br>

## 🟣 이 문서 보는 법

<img src="docs/buttons/click.svg" height="22" alt="클릭"> 처럼 생긴 **보라색 버튼**은 화면에서 **직접 클릭해야 하는 곳**입니다.
버튼에 적힌 글자는 실제 화면의 버튼 이름과 똑같습니다.

`→` 는 "이어서 클릭"을 뜻합니다. 예를 들어

<img src="docs/buttons/settings.svg" height="22" alt="Settings"> → <img src="docs/buttons/secrets-and-variables.svg" height="22" alt="Secrets and variables"> → <img src="docs/buttons/actions.svg" height="22" alt="Actions">

는 `Settings`를 누르고, 이어서 `Secrets and variables`, 그다음 `Actions`를 누르라는 뜻입니다.

`회색 글씨`는 **직접 입력하거나 복사할 값**입니다.

<br>

## 🟣 준비물

- [ ] GitHub 계정
- [ ] 크롬 브라우저
- [ ] **이메일과 비밀번호로 로그인**하는 프로그래머스 계정
  > ⚠️ 구글·카카오·깃허브 등 **소셜 로그인만** 쓰는 계정은 점수·랭킹을 가져올 수 없습니다. [자주 묻는 질문](#-자주-묻는-질문)의 첫 번째 항목을 확인하세요.

<br>

## 🟣 설치하기 (약 10분)

### 1단계. 백준허브 설치

문제를 풀 때마다 GitHub에 자동으로 코드를 올려주는 크롬 확장입니다. 잔디와 연속 기록은 여기 올라간 기록으로 계산합니다.
이미 쓰고 있다면 **2단계로 넘어가세요.**

1. [크롬 웹 스토어의 백준허브 페이지](https://chromewebstore.google.com/detail/ccammcjdkpgjmcpijpahlehmapgmphmk)를 엽니다.
2. <img src="docs/buttons/add-to-chrome.svg" height="22" alt="Chrome에 추가">
3. 브라우저 오른쪽 위 백준허브 아이콘 → <img src="docs/buttons/authorize-with-github.svg" height="22" alt="Authorize with GitHub"> 로 GitHub 계정을 연결합니다.
4. 문제 풀이를 올릴 저장소를 새로 만들거나 기존 저장소를 고른 뒤 <img src="docs/buttons/get-started.svg" height="22" alt="Get Started">
5. 프로그래머스에서 아무 문제나 하나 풀어서, 그 저장소에 `프로그래머스/...` 폴더가 생기는지 확인합니다.

> 📝 이 저장소 이름을 메모해 두세요. 예: `YOUR_GITHUB_ID/algorithm`<br>
> 백준허브는 새 저장소를 **비공개**로 만드는 게 기본값입니다. 비공개라면 3단계가 필요합니다.

### 2단계. 이 템플릿으로 내 저장소 만들기

1. 이 페이지 오른쪽 위에서 <img src="docs/buttons/use-this-template.svg" height="22" alt="Use this template"> → <img src="docs/buttons/create-a-new-repository.svg" height="22" alt="Create a new repository">
2. **Repository name**에 `programmers-streak-badge`를 입력합니다. (다른 이름도 괜찮아요)
3. 공개 범위는 반드시 **Public**으로 둡니다.
   > 비공개 저장소의 이미지는 다른 사람의 프로필 화면에 보이지 않습니다.
4. <img src="docs/buttons/create-repository.svg" height="22" alt="Create repository">

여기서부터는 **방금 만든 내 저장소**에서 진행합니다.

### 3단계. 백준허브 저장소 읽기 토큰 만들기 (비공개일 때만)

백준허브 저장소가 **Public이면 건너뛰세요.**
비공개라면, 배지가 그 저장소의 기록을 **읽기만** 할 수 있는 열쇠(토큰)를 만들어야 합니다.

1. GitHub 오른쪽 위 내 프로필 사진 → <img src="docs/buttons/settings.svg" height="22" alt="Settings">
2. 왼쪽 메뉴 맨 아래 <img src="docs/buttons/developer-settings.svg" height="22" alt="Developer settings">
3. <img src="docs/buttons/personal-access-tokens.svg" height="22" alt="Personal access tokens"> → <img src="docs/buttons/fine-grained-tokens.svg" height="22" alt="Fine-grained tokens"> → <img src="docs/buttons/generate-new-token.svg" height="22" alt="Generate new token">
4. 아래처럼 입력합니다.

   | 항목 | 값 |
   |---|---|
   | Token name | `programmers-streak-read` |
   | Expiration | 원하는 기간 (만료되면 새로 만들어 다시 등록) |
   | Repository access | <img src="docs/buttons/only-select-repositories.svg" height="22" alt="Only select repositories"> → **백준허브 저장소 하나만** 선택 |
   | Permissions → Repository permissions → **Contents** | `Read-only` |

5. 맨 아래 <img src="docs/buttons/generate-token.svg" height="22" alt="Generate token">
6. 화면에 나온 `github_pat_...` 값을 **복사해 둡니다.** 이 화면을 벗어나면 다시 볼 수 없습니다.

### 4단계. 비밀값 등록하기

비밀번호와 토큰은 <b>저장소 비밀값(Secrets)</b>에 넣습니다. 여기 넣은 값은 나를 포함해 누구도 다시 볼 수 없고, 자동 실행할 때만 쓰입니다.

내 배지 저장소에서
<img src="docs/buttons/settings.svg" height="22" alt="Settings"> → <img src="docs/buttons/secrets-and-variables.svg" height="22" alt="Secrets and variables"> → <img src="docs/buttons/actions.svg" height="22" alt="Actions">

아래 값마다 <img src="docs/buttons/new-repository-secret.svg" height="22" alt="New repository secret"> 를 누르고, **Name**과 **Secret**을 입력한 뒤 <img src="docs/buttons/add-secret.svg" height="22" alt="Add secret">

| Name (그대로 복사) | Secret에 넣을 값 | 필수 |
|---|---|---|
| `PROGRAMMERS_ID` | 프로그래머스 로그인 이메일 | ✅ |
| `PROGRAMMERS_PW` | 프로그래머스 비밀번호 | ✅ |
| `ALGO_REPO_TOKEN` | 3단계에서 복사한 `github_pat_...` | 백준허브 저장소가 비공개일 때만 |

### 5단계. 저장소 이름 알려주기

같은 화면에서 <img src="docs/buttons/variables.svg" height="22" alt="Variables"> 탭 → <img src="docs/buttons/new-repository-variable.svg" height="22" alt="New repository variable">

| Name | Value | 예시 |
|---|---|---|
| `ALGO_REPO` | 백준허브 저장소의 `아이디/저장소이름` | `YOUR_GITHUB_ID/algorithm` |

입력 후 <img src="docs/buttons/add-variable.svg" height="22" alt="Add variable">

> (선택) 백준 기록도 잔디에 합치고 싶다면 같은 방법으로 `PLATFORM_DIRS` 변수를 추가하고 값에 `프로그래머스,백준` 을 넣으세요. 등록하지 않으면 `프로그래머스` 폴더만 셉니다.

### 6단계. 첫 실행

자동 실행은 매시간 돌지만, 처음 한 번은 직접 실행해서 잘 되는지 확인합니다.

1. 저장소 위쪽 탭에서 <img src="docs/buttons/actions.svg" height="22" alt="Actions">
2. 왼쪽 목록에서 <img src="docs/buttons/workflow.svg" height="22" alt="Programmers Streak Badge">
3. 오른쪽 <img src="docs/buttons/run-workflow.svg" height="22" alt="Run workflow"> → 펼쳐진 창의 <img src="docs/buttons/run-workflow.svg" height="22" alt="Run workflow">
4. 1~2분 뒤 초록색 체크 ✅ 가 뜨면 성공입니다. 저장소의 `assets/programmers-streak.svg` 파일이 생겼는지 확인하세요.

> ❌ 빨간 X가 떴다면 [자주 묻는 질문](#-자주-묻는-질문)을 확인하세요.

### 7단계. 프로필 README에 붙이기

1. 내 프로필 저장소(`YOUR_GITHUB_ID/YOUR_GITHUB_ID`)로 이동합니다.
   > 없다면 저장소 이름을 **내 아이디와 똑같이** 만들고 Public으로 생성하면 됩니다. GitHub가 그 저장소의 README를 프로필에 보여줍니다.
2. `README.md`를 열고 연필 모양 <img src="docs/buttons/edit.svg" height="22" alt="Edit">
3. 원하는 위치에 아래 코드를 붙여넣고 `YOUR_GITHUB_ID`를 **내 아이디**로 바꿉니다. 2단계에서 저장소 이름을 바꿨다면 그 부분도 바꿉니다.

   ```html
   <p align="center">
     <img src="https://raw.githubusercontent.com/YOUR_GITHUB_ID/programmers-streak-badge/main/assets/programmers-streak.svg"
          alt="Programmers Streak Badge" width="100%">
   </p>
   ```

4. <img src="docs/buttons/commit-changes.svg" height="22" alt="Commit changes..."> → 확인 창의 <img src="docs/buttons/commit-changes-confirm.svg" height="22" alt="Commit changes">

이제 프로필에 배지가 보입니다. 🎉

<br>

## 🟣 (선택) 풀자마자 바로 갱신하기

기본 설정은 **매시간** 갱신입니다. 문제를 풀자마자 배지에 반영되길 원하면, 백준허브 저장소에 "새 풀이가 올라오면 배지 저장소를 깨우는" 작은 자동화를 추가합니다.

**① 배지 저장소를 깨울 수 있는 토큰 만들기**

3단계와 같은 방법으로 토큰을 하나 더 만듭니다. 이번에는

| 항목 | 값 |
|---|---|
| Token name | `programmers-streak-dispatch` |
| Repository access | <img src="docs/buttons/only-select-repositories.svg" height="22" alt="Only select repositories"> → **배지 저장소** 선택 |
| Permissions → **Contents** | `Read and write` |

**② 백준허브 저장소에 비밀값 등록**

**백준허브 저장소**에서 <img src="docs/buttons/settings.svg" height="22" alt="Settings"> → <img src="docs/buttons/secrets-and-variables.svg" height="22" alt="Secrets and variables"> → <img src="docs/buttons/actions.svg" height="22" alt="Actions"> → <img src="docs/buttons/new-repository-secret.svg" height="22" alt="New repository secret">

- Name: `BADGE_DISPATCH_TOKEN`
- Secret: ①에서 만든 토큰

**③ 백준허브 저장소에 파일 추가**

**백준허브 저장소** 첫 화면에서 <img src="docs/buttons/add-file.svg" height="22" alt="Add file"> → <img src="docs/buttons/create-new-file.svg" height="22" alt="Create new file">

파일 이름에 `.github/workflows/notify-badge.yml` 을 입력하고, 아래 내용을 붙여넣습니다. `YOUR_GITHUB_ID`는 내 아이디로 바꿉니다. 2단계에서 저장소 이름을 바꿨다면 `programmers-streak-badge` 부분도 바꿉니다.

```yaml
name: notify-badge
on:
  push:
    branches: [main]
jobs:
  dispatch:
    runs-on: ubuntu-latest
    steps:
      - run: |
          curl -sS -X POST \
            -H "Authorization: Bearer ${{ secrets.BADGE_DISPATCH_TOKEN }}" \
            -H "Accept: application/vnd.github+json" \
            https://api.github.com/repos/YOUR_GITHUB_ID/programmers-streak-badge/dispatches \
            -d '{"event_type":"solved"}'
```

<img src="docs/buttons/commit-changes.svg" height="22" alt="Commit changes..."> → 확인 창의 <img src="docs/buttons/commit-changes-confirm.svg" height="22" alt="Commit changes">

이제 문제를 풀면 1~2분 안에 배지가 바뀝니다.

<br>

## 🟣 배지 읽는 법

<img src="docs/preview-pending.png" alt="오늘 아직 안 푼 상태" width="100%">

| 표시 | 뜻 |
|---|---|
| **Score · Rank · Solved** | 프로그래머스 내 정보의 점수, 전체 랭킹, 해결한 문제 수 |
| **27 days in a row** | 현재 연속으로 푼 날 수 |
| **Best streak** | 지금까지 가장 길게 이어간 연속 기록 |
| ✓ `SOLVED TODAY` (체크 원) | 오늘 이미 풀었음 |
| ⧗ `NOT YET TODAY` (모래시계, 깜빡임) | 오늘 아직 안 풀었음. 자정 전에 풀면 연속 기록이 이어집니다 |
| 잔디 칸 색 | 그날 푼 문제 수. 흐린 분홍 → 흰색으로 갈수록 많이 푼 날 |
| **주황 테두리 칸** | 안 푼 날 |
| 흰 테두리 칸 | 오늘 |

> 잔디·연속 기록은 백준허브가 올린 기록으로, 점수·랭킹·해결한 문제 수는 프로그래머스 계정 정보로 계산합니다.
> 그래서 백준허브를 쓰기 전에 푼 문제는 잔디에는 없지만 **Solved 숫자에는 포함**됩니다.

<br>

## 🟣 자주 묻는 질문

<details>
<summary><b>Q. 소셜 로그인으로 가입했어요</b></summary>
<br>

점수·랭킹·해결한 문제 수는 이메일과 비밀번호로 로그인해야 가져올 수 있습니다.
프로그래머스 계정 설정에서 이메일 로그인용 비밀번호를 설정할 수 있는지 확인해 보세요.

비밀번호 없이 쓰면 왼쪽 Stats는 `—` 로 표시되고, **오른쪽 연속 기록과 잔디는 정상 동작**합니다. 이 경우 4단계의 `PROGRAMMERS_ID`, `PROGRAMMERS_PW`는 등록하지 않아도 됩니다.
</details>

<details>
<summary><b>Q. Score·Rank·Solved가 <code>—</code> 로 나와요</b></summary>
<br>

- 4단계의 `PROGRAMMERS_ID`(이메일), `PROGRAMMERS_PW` 값이 맞는지 확인하세요. 비밀값은 다시 볼 수 없으니 틀린 것 같으면 같은 이름으로 다시 등록하면 덮어써집니다.
- 프로그래머스 사이트 사정으로 일시적으로 실패하면, **마지막으로 성공한 값**을 그대로 보여줍니다. 한 번도 성공한 적이 없을 때만 `—` 가 나옵니다.
</details>

<details>
<summary><b>Q. 잔디가 비어 있거나 연속 기록이 0이에요</b></summary>
<br>

- 5단계의 `ALGO_REPO` 값이 `아이디/저장소이름` 형식으로 정확한지 확인하세요.
- 백준허브 저장소가 비공개인데 `ALGO_REPO_TOKEN`을 등록하지 않았거나, 토큰에 그 저장소가 선택되지 않았을 수 있습니다. (3단계)
- 백준허브 저장소 안에 `프로그래머스` 폴더가 있는지 확인하세요.
</details>

<details>
<summary><b>Q. 6단계에서 빨간 X가 떴어요</b></summary>
<br>

- 실행 기록에 `ALGO_REPO 변수를 등록하세요` 가 보이면 5단계를 하지 않은 것입니다. 5단계를 마친 뒤 다시 실행하세요. (템플릿으로 저장소를 만든 직후에는 5단계 전까지 매시간 실행이 이 오류로 실패하는데, 정상입니다.)
- `Checkout algorithm repo` 단계에서 실패했다면 `ALGO_REPO` 철자, 또는 비공개 저장소의 `ALGO_REPO_TOKEN`(3단계)을 확인하세요.
- `push` 단계에서 권한 오류(403)가 났다면 아래처럼 쓰기 권한을 켭니다.

내 배지 저장소에서
<img src="docs/buttons/settings.svg" height="22" alt="Settings"> → 왼쪽 <img src="docs/buttons/actions.svg" height="22" alt="Actions"> → <img src="docs/buttons/general.svg" height="22" alt="General">

아래로 내려 **Workflow permissions**에서 <img src="docs/buttons/read-and-write-permissions.svg" height="22" alt="Read and write permissions"> 선택 → <img src="docs/buttons/save.svg" height="22" alt="Save">

그다음 6단계를 다시 실행하세요.
</details>

<details>
<summary><b>Q. 문제를 풀었는데 배지가 안 바뀌어요</b></summary>
<br>

- 기본 갱신 주기는 1시간입니다. 바로 보고 싶으면 6단계처럼 직접 실행하거나 [풀자마자 갱신](#-선택-풀자마자-바로-갱신하기)을 설정하세요.
- GitHub가 이미지를 몇 분간 캐시합니다. 새로고침(Ctrl+F5 / Cmd+Shift+R) 해 보세요.
- 백준허브가 실제로 커밋했는지 백준허브 저장소에서 확인하세요.
</details>

<details>
<summary><b>Q. 60일 동안 저장소에 변화가 없으면 자동 실행이 멈춘다던데요?</b></summary>
<br>

GitHub는 오랫동안 활동이 없는 저장소의 예약 실행을 멈춥니다. 이 배지는 값이 바뀔 때마다 커밋하므로 꾸준히 풀고 있다면 문제없습니다.
멈췄다면 <img src="docs/buttons/actions.svg" height="22" alt="Actions"> 탭 상단 안내에 따라 다시 켜고 6단계를 실행하세요.
</details>

<br>

## 🟣 보안 안내

- 프로그래머스 비밀번호는 <b>내 저장소의 비밀값(Secrets)</b>에만 저장되고, 코드·실행 기록(로그)·커밋 어디에도 남지 않습니다.
- 토큰은 꼭 필요한 저장소 하나, 꼭 필요한 권한(읽기 전용)만 주도록 안내했습니다.
- 점수·랭킹은 프로그래머스가 **공식으로 공개한 API가 아니라** 웹사이트가 내부적으로 쓰는 주소에서 가져옵니다. 프로그래머스가 사이트를 바꾸면 갑자기 동작하지 않을 수 있습니다.
- 걱정된다면 `PROGRAMMERS_ID`, `PROGRAMMERS_PW`를 등록하지 않아도 됩니다. 연속 기록과 잔디는 그대로 동작합니다.

<br>

## 🟣 크레딧

- 점수·랭킹을 가져오는 방식은 [tomy8964/Programmers_Badge_Generator](https://github.com/tomy8964/Programmers_Badge_Generator)와 [libtv/github-programmers-rank](https://github.com/libtv/github-programmers-rank)를 참고했습니다.
- 풀이 기록은 [백준허브(BaekjoonHub)](https://github.com/BaekjoonHub/BaekjoonHub)가 올려준 커밋을 사용합니다.
- 글꼴: [Hanken Grotesk](https://github.com/marcologous/hanken-grotesk), [Instrument Serif](https://github.com/Instrument/instrument-serif) — SIL Open Font License 1.1
- 이 프로젝트는 프로그래머스(그렙)와 관련이 없는 개인 프로젝트입니다.
