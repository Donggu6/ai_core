from app.report.gpt_writer import write_gpt_report

def write_report(product, features, score):
    try:
        return write_gpt_report(product, features, score)
    except Exception as e:
        print("GPT REPORT ERROR:", e)
        return "AI 분석 리포트 생성 중 오류가 발생했습니다."
