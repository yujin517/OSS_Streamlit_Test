import streamlit as st
import pandas as pd

st.set_page_config(page_title="성향 기반 취미 추천 테스트", page_icon="assets/hobby.png")

STUDENT_ID = "2024404036"
STUDENT_NAME = "임유진"

USER_ID = "임유진"
USER_PW = "1234"


@st.cache_data
def load_quiz_data():
    return pd.read_csv("data/quiz_data.csv")


def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "current_q" not in st.session_state:
        st.session_state.current_q = 0

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    if "show_result_page" not in st.session_state:
        st.session_state.show_result_page = False

    if "final_scores" not in st.session_state:
        st.session_state.final_scores = None


def login():
    st.subheader("로그인")

    user_id = st.text_input("아이디")
    user_pw = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        if user_id == USER_ID and user_pw == USER_PW:
            st.session_state.logged_in = True
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")


def show_result(scores):
    result_type = max(scores, key=scores.get)

    result_info = {
        "활동형": {
            "title": "주말 액티비티 탐험가",
            "emoji": "🏃‍♀️",
            "desc": "가만히 있기보다 직접 움직이고 경험하면서 에너지를 얻는 타입입니다.",
            "hobbies": ["테니스 치기", "등산 가기", "클라이밍", "서핑", "캠핑 가기"],
            "tip": "처음부터 장비를 많이 사기보다 원데이 클래스나 체험권으로 가볍게 시작해보세요.",
            "mission": "이번 주에는 30분 이상 몸을 움직이는 활동 하나를 해보기",
        },
        "휴식형": {
            "title": "느긋한 방구석 충전러",
            "emoji": "🛋️",
            "desc": "복잡한 자극보다 편안한 공간에서 천천히 에너지를 회복하는 타입입니다.",
            "hobbies": ["산책하기", "넷플릭스 감상", "요가 배우기", "음악 감상", "컬러링북 칠하기"],
            "tip": "취미를 성과로 만들기보다 쉬는 시간을 잘 보내는 방식으로 접근해보세요.",
            "mission": "이번 주에는 좋아하는 음악을 들으면서 20분 산책하기",
        },
        "분석형": {
            "title": "차분한 성장 수집가",
            "emoji": "📚",
            "desc": "새로운 지식을 쌓고 실력이 늘어나는 과정에서 만족감을 느끼는 타입입니다.",
            "hobbies": ["외국어 공부", "자격증 따기", "경제 공부하기", "프로그래밍하기", "독서"],
            "tip": "작은 목표를 정하고 기록하면 오래 지속하기 좋습니다.",
            "mission": "이번 주에는 관심 있는 분야 강의나 글 하나를 정리해보기",
        },
        "감성형": {
            "title": "감성 기록 아티스트",
            "emoji": "🎨",
            "desc": "감각과 감정을 표현하거나 아름다운 것을 경험할 때 즐거움을 느끼는 타입입니다.",
            "hobbies": ["사진 찍기", "그림 그리기", "다이어리 꾸미기", "전시회 가기", "악기 배우기"],
            "tip": "잘하려고 하기보다 내 취향을 남기는 과정 자체를 즐겨보세요.",
            "mission": "이번 주에는 마음에 드는 장면 하나를 사진이나 글로 기록하기",
        },
        "사교형": {
            "title": "취미 공유 네트워커",
            "emoji": "🤝",
            "desc": "혼자보다 사람들과 함께할 때 더 큰 즐거움과 동기부여를 얻는 타입입니다.",
            "hobbies": ["맛집 투어", "독서 모임", "공연 보러 가기", "야구장 직관", "자원봉사"],
            "tip": "동호회나 소모임처럼 함께할 수 있는 환경을 만들면 취미가 더 오래 갑니다.",
            "mission": "이번 주에는 친구 한 명에게 같이 해보고 싶은 활동을 제안하기",
        },
    }

    info = result_info[result_type]

    st.success("분석 완료!")
    st.header(f"{info['emoji']} 당신은『{info['title']}』타입입니다")
    st.write(info["desc"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("추천 취미")
        for hobby in info["hobbies"]:
            st.write(f"- {hobby}")

    with col2:
        st.subheader("시작 팁")
        st.write(info["tip"])

        st.subheader("이번 주 미션")
        st.write(info["mission"])

    with st.expander("유형별 점수 자세히 보기"):
        st.write(scores)


def calculate_scores():
    scores = {
        "활동형": 0,
        "휴식형": 0,
        "분석형": 0,
        "감성형": 0,
        "사교형": 0,
    }

    for answer in st.session_state.answers.values():
        scores[answer["type"]] += 1

    return scores


def reset_test():
    st.session_state.current_q = 0
    st.session_state.answers = {}
    st.session_state.show_result_page = False
    st.session_state.final_scores = None


def main():
    init_session()

    st.title("성향 기반 취미 추천 테스트")
    st.info(f"학번: {STUDENT_ID} / 이름: {STUDENT_NAME}")

    st.write(
        "나의 성향과 가까운 답변을 선택하면, 답변을 점수화하여 잘 맞는 취미 유형을 추천해주는 테스트입니다."
    )

    if not st.session_state.logged_in:
        login()
        return

    st.success("로그인 상태입니다.")

    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.rerun()

    st.divider()

    quiz_data = load_quiz_data()

    if st.session_state.show_result_page:
        show_result(st.session_state.final_scores)

        if st.button("다시 테스트하기"):
            reset_test()
            st.rerun()

        return

    st.subheader("취미 성향 퀴즈")

    total_questions = len(quiz_data)
    current_q = st.session_state.current_q
    row = quiz_data.iloc[current_q]

    st.progress((current_q + 1) / total_questions)
    st.caption(f"{current_q + 1} / {total_questions}")

    st.markdown(f"### Q{current_q + 1}. {row['question']}")

    options = [
        row["option_1"],
        row["option_2"],
        row["option_3"],
        row["option_4"],
    ]

    selected_answer = st.session_state.answers.get(current_q)

    for i, option in enumerate(options, start=1):
        if st.button(option, key=f"option_{current_q}_{i}", use_container_width=True):
            selected_type = row[f"type_{i}"]

            st.session_state.answers[current_q] = {
                "option": option,
                "type": selected_type,
            }

            if current_q < total_questions - 1:
                st.session_state.current_q += 1

            st.rerun()

    if current_q < total_questions - 1:
        col_prev, col_blank = st.columns([1, 5])

        with col_prev:
            if st.button("← 이전"):
                if st.session_state.current_q > 0:
                    st.session_state.current_q -= 1
                    st.rerun()

    else:
        col_prev, col_result = st.columns([1, 5])

        with col_prev:
            if st.button("← 이전"):
                if st.session_state.current_q > 0:
                    st.session_state.current_q -= 1
                    st.rerun()

        with col_result:
            if st.button("결과 확인", use_container_width=True):
                if current_q in st.session_state.answers:
                    st.session_state.final_scores = calculate_scores()
                    st.session_state.show_result_page = True
                    st.rerun()
                else:
                    st.error("마지막 문항에 답변해주세요.")


if __name__ == "__main__":
    main()