## 장인후 (Inhu Chang)

사회복지를 공부하고 사회복지 현장과 사회적기업 재단에서 15년 정도 일했습니다. 앞으로 사회복지 영역에서도 AI를 쓰는 일이 많아질 텐데, 그때 필요한 것은 AI를 쓸 줄 아는 것보다 믿을 수 있는 지식을 바탕으로 사람이 AI를 잘 활용하도록 돕는 도구라고 생각합니다. 그래서 지금은 컴퓨터공학을 공부하면서, 잘 정리된 지식 데이터베이스 위에서 작동하는 AI 도구를 제 공부와 연구에 먼저 만들어 쓰고 있습니다. 장기적으로는 이를 아동빈곤과 사회정책 연구로 이어가고 싶습니다.

### 요즘 하는 일

#### 이룸 (irum)
논문을 찾고, 읽고, 쓰는 일을 한 프로그램에서 하는 Mac 앱입니다. 지금 초기 버전을 마무리하고 있습니다.
처음에는 논문을 정독하는 도구(Reading Companion)를 따로 만들었습니다. 그런데 쓰다 보니 찾은 논문, 읽으며 남긴 메모, 쓰는 원고가 서로 떨어져 있는 게 문제였습니다. 그래서 그 도구를 바탕으로 세 가지를 하나로 묶은 것이 이룸입니다.

- 찾기: 씨앗 논문에서 관련 논문을 넓혀 갑니다(OpenAlex, KCI). Zotero 서재도 불러옵니다.
- 읽기: PDF에서 본문·수식·표를 뽑아 원문과 번역을 나란히 놓고 읽으며 메모합니다.
- 쓰기: LaTeX 원고를 편집·컴파일하고, AI 채팅과 음성 받아쓰기, 발표 모드도 넣었습니다.
- 세 화면이 논문 저장소 하나를 같이 씁니다. 이 서재를 MCP 서버로 열어 두어서, 앱 밖의 Claude Code나 Codex도 내 논문을 찾고 읽는 도구로 쓸 수 있습니다.
- AI가 쓴 요약은 문장 단위로 쪼개 원문과 하나씩 대조해 검증합니다. 요약하는 모델과 검증하는 모델은 서로 다른 회사 모델을 씁니다.
- 작업 폴더마다 지시문과 기억을 두고 AI에게 일을 맡기는데, AI가 도구를 쓸 때마다 허락을 받게 했습니다.

#### 스트렝 선형대수 스터디
스트렝 교재와 MIT 강의로 스터디를 하고 있습니다. 강의 자막을 쉬운 노트로 바꾸고, 공부하면서 생긴 질문과 답을 날짜별로 모으고 있습니다. 같은 노트를 오픈 웨이트 모델 다섯 개에게 써보게 하고 이름을 가린 채 비교해 보기도 했는데, 가장 작은 27B 모델이 제일 나았습니다. 이 실험과, 할루시네이션을 막고 원문과 대조하는 제 작업 규칙은 [lecture-note-bench](https://github.com/yamf97/lecture-note-bench)에 공개해 두었습니다.

다음에는 스터디 녹화를 전사해서 자료로 만들고, 스터디와 수학 커뮤니티에서 자주 나오는 질문을 모아 답변 데이터베이스를 만들 생각입니다. 이걸 RAG와 온톨로지로 묶고, 파인튜닝까지 해서 MCP로 LLM에 붙여보려고 합니다. 아직 설계 단계입니다.

#### 그 밖에
계량경제학(Angrist & Pischke)과 Agent AI 강의 스터디 노트·발표 자료, 영어 쉐도잉 앱을 만들고 있습니다.

전에 수학 커뮤니티 자료로 AI 학습 도구를 만들자는 제안서를 함께 쓴 적이 있습니다. 실행하지는 않았지만, 지금 스터디 작업은 그때 생각에서 시작됐습니다.

대부분 비공개 저장소입니다. 궁금한 게 있으면 연락 주세요.

Python · JavaScript/TypeScript · Electron · Claude/Gemini API · MCP · RAG · Obsidian · LaTeX

텍사스주 텍사캐나

---

### In English

I spent about fifteen years in social welfare, both in the field and at a social enterprise foundation. AI will soon reach social welfare work too. What will matter most, I think, are tools grounded in trustworthy knowledge that help people use AI well. So I now study computer science, and I build those tools for my own study and research first.

#### irum
A Mac app that brings finding, reading, and writing papers into one place. I'm wrapping up its first version now. It grew out of my earlier close-reading tool, Reading Companion.

- **Find**: expand from a seed paper to related work (OpenAlex, KCI) and import a Zotero library
- **Read**: original and translation side by side, with notes
- **Write**: LaTeX editing and compiling, with AI chat
- One shared paper library, also exposed over MCP so agents like Claude Code can search and read it

#### Strang linear algebra study
- Plain-language notes from the lecture subtitles, plus a dated Q&A log
- A blind comparison of five open-weight models writing the same note (the smallest, a 27B model, did best)
- Next: a study-group Q&A database combining RAG, an ontology, and fine-tuning, served over MCP (design stage)

My long-term research interest is child poverty and social policy. Most repos are private, so feel free to reach out.
