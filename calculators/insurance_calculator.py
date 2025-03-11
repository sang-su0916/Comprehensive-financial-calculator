import streamlit as st
import pandas as pd
import numpy as np

def insurance_calculator():
    st.header("보장계산기")
    
    # 사용 방법 안내
    with st.expander("💡 보장계산기 사용 방법"):
        st.write("""
        이 계산기는 가족의 미래를 보장하기 위해 필요한 보험금을 계산해 드립니다:
        
        1. 개인 정보와 가족 상황을 입력하세요.
        2. 현재 보유한 자산과 보험 정보를 입력하세요.
        3. '계산하기' 버튼을 클릭하여 필요한 보장 금액을 확인하세요.
        """)
    
    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["기본 정보", "자산 정보", "보험 정보"])
    
    with tab1:
        # 기본 정보 입력
        st.subheader("가족 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("가장의 현재 나이", min_value=20, max_value=80, value=40)
            dependents = st.number_input("자녀 수", min_value=0, max_value=10, value=3)
            spouse_exists = st.checkbox("배우자 유무", value=True)
            
            if spouse_exists:
                spouse_age = st.number_input("배우자의 나이", min_value=20, max_value=80, value=38)
                spouse_retirement_age = st.number_input("배우자의 은퇴 희망 나이", min_value=spouse_age, max_value=90, value=65)
        
        with col2:
            annual_income_text = st.text_input(
                "현재 연소득 (원)",
                value="60,000,000",
                help="숫자만 입력하세요. 예: 60000000"
            )
            try:
                annual_income = int(annual_income_text.replace(',', ''))
            except:
                annual_income = 60000000
            
            monthly_living_expenses_text = st.text_input(
                "월 생활비 (원)",
                value="3,000,000",
                help="숫자만 입력하세요. 예: 3000000"
            )
            try:
                monthly_living_expenses = int(monthly_living_expenses_text.replace(',', ''))
            except:
                monthly_living_expenses = 3000000
            
            current_debt_text = st.text_input(
                "현재 대출 잔액 (원)",
                value="200,000,000",
                help="숫자만 입력하세요. 예: 200000000"
            )
            try:
                current_debt = int(current_debt_text.replace(',', ''))
            except:
                current_debt = 200000000
        
        # 어린 자녀 정보
        if dependents > 0:
            st.subheader("자녀 정보")
            children_ages = []
            
            cols = st.columns(min(4, dependents))
            for i in range(dependents):
                with cols[i % len(cols)]:
                    child_age = st.number_input(f"{i+1}번째 자녀 나이", min_value=0, max_value=30, value=min(i*3, 18))
                    children_ages.append(child_age)
    
    with tab2:
        # 자산 정보 입력
        st.subheader("보유 자산 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cash_savings_text = st.text_input(
                "현금 및 예금 (원)",
                value="30,000,000",
                help="현금, 예금, CMA 등 즉시 사용 가능한 자금"
            )
            try:
                cash_savings = int(cash_savings_text.replace(',', ''))
            except:
                cash_savings = 30000000
            
            stocks_text = st.text_input(
                "주식 및 펀드 (원)",
                value="20,000,000",
                help="주식, ETF, 펀드 등 금융투자 자산"
            )
            try:
                stocks = int(stocks_text.replace(',', ''))
            except:
                stocks = 20000000
            
            bonds_text = st.text_input(
                "채권 (원)",
                value="10,000,000",
                help="국채, 회사채 등의 채권형 자산"
            )
            try:
                bonds = int(bonds_text.replace(',', ''))
            except:
                bonds = 10000000
        
        with col2:
            real_estate_text = st.text_input(
                "부동산 (원)",
                value="150,000,000",
                help="부동산 투자 자산(주택 제외)"
            )
            try:
                real_estate = int(real_estate_text.replace(',', ''))
            except:
                real_estate = 150000000
            
            retirement_accounts_text = st.text_input(
                "연금 및 퇴직금 (원)",
                value="40,000,000",
                help="국민연금, 퇴직연금, 개인연금 등의 적립금"
            )
            try:
                retirement_accounts = int(retirement_accounts_text.replace(',', ''))
            except:
                retirement_accounts = 40000000
            
            other_assets_text = st.text_input(
                "기타 자산 (원)",
                value="5,000,000",
                help="자동차, 귀금속 등 기타 자산"
            )
            try:
                other_assets = int(other_assets_text.replace(',', ''))
            except:
                other_assets = 5000000
        
        # 총 자산 계산 및 표시
        total_assets = cash_savings + stocks + bonds + real_estate + retirement_accounts + other_assets
        
        # 자산 배분 차트
        st.subheader(f"총 자산: ₩{total_assets:,.0f}")
        asset_data = {
            "자산유형": ["현금 및 예금", "주식 및 펀드", "채권", "부동산", "연금 및 퇴직금", "기타 자산"],
            "금액": [cash_savings, stocks, bonds, real_estate, retirement_accounts, other_assets]
        }
        asset_df = pd.DataFrame(asset_data)
        asset_df["비율"] = asset_df["금액"] / total_assets * 100
        
        # 자산 비율 표시
        st.write("**자산별 비중:**")
        cols = st.columns(3)
        for i, row in enumerate(asset_df.itertuples()):
            with cols[i % 3]:
                st.metric(row.자산유형, f"₩{row.금액:,.0f}", f"{row.비율:.1f}%")
    
    with tab3:
        # 현재 보험 정보
        st.subheader("현재 보험 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            life_insurance_text = st.text_input(
                "생명보험 보장금액 (원)",
                value="100,000,000",
                help="사망 보장 금액의 합계"
            )
            try:
                life_insurance = int(life_insurance_text.replace(',', ''))
            except:
                life_insurance = 100000000
            
            disability_insurance_text = st.text_input(
                "소득보장보험 월 보장금액 (원)",
                value="1,000,000",
                help="장애 발생 시 받게 되는 월 보장금액"
            )
            try:
                disability_insurance = int(disability_insurance_text.replace(',', ''))
            except:
                disability_insurance = 1000000
        
        with col2:
            critical_illness_insurance_text = st.text_input(
                "중대질병보험 보장금액 (원)",
                value="50,000,000",
                help="중대질병 진단금 및 의료비 보장 합계"
            )
            try:
                critical_illness_insurance = int(critical_illness_insurance_text.replace(',', ''))
            except:
                critical_illness_insurance = 50000000
            
            monthly_premium_text = st.text_input(
                "월 보험료 지출 (원)",
                value="300,000",
                help="모든 보험에 지출하는 월 보험료 합계"
            )
            try:
                monthly_premium = int(monthly_premium_text.replace(',', ''))
            except:
                monthly_premium = 300000
    
    if st.button("계산하기", key="insurance_button", use_container_width=True):
        # 총 가용 자산 (유동성 자산 + 일부 투자 자산만 고려)
        liquid_assets = cash_savings + stocks * 0.7 + bonds * 0.9  # 주식은 70%, 채권은 90% 가용성 가정
        
        # 필요 보장금 계산
        results = calculate_insurance_needs(
            age=age,
            annual_income=annual_income,
            monthly_expenses=monthly_living_expenses,
            dependents=dependents,
            children_ages=children_ages if dependents > 0 else [],
            spouse_exists=spouse_exists,
            spouse_age=spouse_age if spouse_exists else None,
            debt=current_debt,
            liquid_assets=liquid_assets,
            total_assets=total_assets
        )
        
        # 현재 보험 상태
        current_coverage = {
            "생명보험": life_insurance,
            "소득보장": disability_insurance * 12,  # 연간으로 변환
            "중대질병": critical_illness_insurance
        }
        
        # 보장 갭 계산
        coverage_gap = {
            category: results[category] - current_coverage.get(category, 0)
            for category in results
        }
        
        # 결과 표시: 탭으로 구성
        result_tab1, result_tab2 = st.tabs(["보장 현황", "보장 분석"])
        
        with result_tab1:
            st.subheader("📊 보장 분석 결과")
            
            # 요약 정보
            total_needed = sum(results.values())
            total_current = sum(current_coverage.values())
            total_gap = total_needed - total_current
            
            col1, col2, col3 = st.columns(3)
            col1.metric("필요 총 보장액", f"₩{total_needed:,.0f}")
            col2.metric("현재 총 보장액", f"₩{total_current:,.0f}")
            
            if total_gap > 0:
                col3.metric("보장 부족액", f"₩{total_gap:,.0f}", delta=f"-{total_gap/total_needed*100:.1f}%", delta_color="inverse")
            else:
                col3.metric("보장 초과액", f"₩{-total_gap:,.0f}", delta=f"+{-total_gap/total_needed*100:.1f}%", delta_color="normal")
            
            # 자산 및 위험 노출 요약
            st.markdown("---")
            st.subheader("자산 및 위험 노출 분석")
            
            # 자산과 부채 비교
            assets_vs_debt = st.columns(2)
            with assets_vs_debt[0]:
                st.metric("총 자산", f"₩{total_assets:,.0f}")
            with assets_vs_debt[1]:
                st.metric("총 부채", f"₩{current_debt:,.0f}", 
                         f"자산의 {current_debt/total_assets*100:.1f}%", 
                         delta_color="inverse" if current_debt > total_assets * 0.5 else "normal")
            
            # 유동성 자산 분석
            liquidity_metrics = st.columns(2)
            with liquidity_metrics[0]:
                st.metric("가용 자산(유동성)", f"₩{liquid_assets:,.0f}", 
                         f"총 자산의 {liquid_assets/total_assets*100:.1f}%")
            with liquidity_metrics[1]:
                emergency_months = liquid_assets / monthly_living_expenses
                st.metric("비상자금 준비기간", f"{emergency_months:.1f}개월",
                         "충분함" if emergency_months >= 6 else "부족함",
                         delta_color="normal" if emergency_months >= 6 else "inverse")
            
            # 월 보험료 부담 분석
            insurance_burden = monthly_premium / monthly_living_expenses * 100
            st.metric("월 보험료 부담률", f"{insurance_burden:.1f}%", 
                     "적정" if insurance_burden <= 15 else "과다",
                     delta_color="normal" if insurance_burden <= 15 else "inverse")
        
        with result_tab2:
            # 상세 분석
            st.subheader("보장 유형별 분석")
            
            for category in results:
                need = results[category]
                current = current_coverage.get(category, 0)
                gap = coverage_gap[category]
                
                col1, col2, col3 = st.columns(3)
                col1.metric(f"{category} 필요액", f"₩{need:,.0f}")
                col2.metric(f"현재 {category}", f"₩{current:,.0f}")
                
                if gap > 0:
                    col3.metric("부족액", f"₩{gap:,.0f}", delta=f"-{gap/need*100:.1f}%" if need > 0 else "", delta_color="inverse")
                    st.warning(f"{category} 보장이 부족합니다. 추가 가입을 고려하세요.")
                else:
                    col3.metric("초과액", f"₩{-gap:,.0f}", delta=f"+{-gap/need*100:.1f}%" if need > 0 else "", delta_color="normal")
                    st.success(f"{category} 보장이 충분합니다.")
                
                st.write("---")
            
            # 조언
            st.subheader("📝 보장 개선 제안")
            
            insufficient = [k for k, v in coverage_gap.items() if v > 0]
            if insufficient:
                for area in insufficient:
                    if area == "생명보험":
                        st.write("- **생명보험**: 정기 생명보험으로 보장을 강화하세요. 특히 소득원이 되는 가장에게 중요합니다.")
                        if current_debt > 0:
                            st.write(f"  - 최소한 현재 부채 ₩{current_debt:,.0f}원을 갚을 수 있는 보장은 필요합니다.")
                        if dependents > 0:
                            education_cost = len([age for age in children_ages if age < 19]) * 100000000
                            st.write(f"  - 자녀 교육비로 약 ₩{education_cost:,.0f}원이 필요할 것으로 예상됩니다.")
                    elif area == "소득보장":
                        st.write("- **소득보장**: 장기 장애 발생 시 소득을 대체할 수 있는 소득보장보험을 고려하세요.")
                        st.write(f"  - 월 최소 ₩{monthly_living_expenses:,.0f}원의 생활비를 감당할 수 있어야 합니다.")
                    elif area == "중대질병":
                        st.write("- **중대질병**: 암, 뇌졸중, 심근경색 등 중대 질병 발생 시 경제적 부담을 덜어줄 수 있는 보험을 검토하세요.")
                        st.write(f"  - 치료비와 회복 기간 동안의 소득 감소를 고려해야 합니다.")
                
                st.info("💡 **최적화 제안**: 현재 월 보험료가 생활비의 15%를 초과한다면, 보장 내용은 유지하면서 보험료를 줄일 수 있는 방법을 보험 전문가와 상담해보세요.")
            else:
                st.success("👍 현재 모든 영역의 보장이 충분합니다. 정기적으로 상황 변화에 따라 재검토하세요.")
                
                if emergency_months < 6:
                    st.warning("⚠️ 비상자금이 부족합니다. 최소 6개월 이상의 생활비를 유동성 자산으로 보유하는 것이 좋습니다.")
                
                if insurance_burden > 15:
                    st.warning("⚠️ 월 보험료 부담이 생활비의 15%를 초과합니다. 보장 내용은 유지하면서 보험료를 줄일 수 있는 방법을 검토해보세요.")

def calculate_insurance_needs(age, annual_income, monthly_expenses, dependents, children_ages, spouse_exists, spouse_age, debt, liquid_assets, total_assets):
    """필요한 보험 보장금액을 계산합니다."""
    results = {}
    
    # 생명보험 필요액 (소득 대체 + 부채 + 자녀 교육비 - 유동성 자산)
    years_to_retirement = 65 - age
    income_replacement_years = min(years_to_retirement, 20)  # 최대 20년간 소득 대체
    income_replacement = annual_income * 0.7 * income_replacement_years  # 소득의 70%
    
    # 자녀 교육비 (대학교 4년 기준, 1인당 1억원 가정)
    education_costs = 0
    for child_age in children_ages:
        if child_age < 19:
            education_costs += 100000000  # 자녀당 1억원
    
    # 유동성 자산 공제 (비상자금 일부는 제외)
    emergency_fund = monthly_expenses * 6  # 6개월치 생활비는 비상자금으로 남겨둠
    available_liquid_assets = max(0, liquid_assets - emergency_fund)
    
    life_insurance_need = income_replacement + debt + education_costs - available_liquid_assets
    life_insurance_need = max(0, life_insurance_need)
    
    # 소득보장보험 필요액 (연간 소득의 60% - 비상자금의 이자소득 가정)
    emergency_fund_income = emergency_fund * 0.03  # 비상자금의 연 3% 수익 가정
    disability_need = annual_income * 0.6 - (emergency_fund_income / 12)
    disability_need = max(0, disability_need) * 12  # 연간 금액으로 변환
    
    # 중대질병보험 필요액 (연간 소득의 3배 + 치료비 5천만원 가정 - 일부 유동자산)
    treatment_cost = 50000000  # 기본 치료비 가정
    income_loss = annual_income * 3  # 3년간의 소득 손실 가정
    critical_illness_need = treatment_cost + income_loss - (available_liquid_assets * 0.5)  # 유동자산의 50%만 사용 가정
    critical_illness_need = max(0, critical_illness_need)
    
    results["생명보험"] = life_insurance_need
    results["소득보장"] = disability_need
    results["중대질병"] = critical_illness_need
    
    return results
