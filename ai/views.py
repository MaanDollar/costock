from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Stock, StockCorrelation
import requests
import FinanceDataReader as fdr
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
matplotlib.use('Agg')
from django.http import JsonResponse


def price(request, stock_code):
    try:
        # 주식 데이터를 동적으로 가져옴
        stock_df = fdr.DataReader(stock_code, '2023-06-01', '2024-07-26')

        # 당일 마지막 가격과 가격 변화율 계산
        latest_data = stock_df.iloc[-1]  # 마지막 행
        close_price = latest_data['Close']  # 마지막 종가
        change_rate = latest_data['Change'] * 100  # 변화율(%)

        # Matplotlib 그래프 생성
        plt.figure(figsize=(10, 6))
        stock_df['Close'].plot(title=f'Stock Prices for {stock_code}')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.tight_layout()

        # 그래프를 메모리에 저장
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        # 그래프를 base64로 인코딩
        graph_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        # JSON 데이터 생성
        response_data = {
            'stock_code': stock_code,
            'close_price': close_price,
            'change_rate': round(change_rate, 2),  # 소수점 2자리로 반올림
            'graph': graph_base64,
        }

        return JsonResponse(response_data)

    except Exception as e:
        # 에러 발생 시 JSON 에러 응답
        return JsonResponse({
            'error': f"Unable to fetch data for stock code: {stock_code}. Error: {str(e)}"
        }, status=500)

def correlations(request, stock_code1, stock_code2):
    try:
        correlation = StockCorrelation.objects.filter(
            StockCode=stock_code1, RelatedStockCode=stock_code2
        ).first()

        if not correlation:
            correlation = StockCorrelation.objects.filter(
                StockCode=stock_code2, RelatedStockCode=stock_code1
            ).first()

        if not correlation:
            return JsonResponse(
                {"error": f"No correlation found for {stock_code1} and {stock_code2}"},
                status=404
            )

        response_data = {
            "stock_code1": stock_code1,
            "stock_code2": stock_code2,
            "correlation": float(correlation.Correlation),
        }

        return JsonResponse(response_data)

    except Exception as e:
        # 에러 발생 시 JSON 에러 메시지 반환
        return JsonResponse({"error": str(e)}, status=400)

def articles(request):
    try:
        ######practice####
        stock_code1 = "005930"
        stock_code2 = "000660"
        search_query = f"{stock_code1} {stock_code2}"

        api_url = "https://openapi.naver.com/v1/search/news.json"
        headers = {
            "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
        }
        params = {
            "query": search_query,
            "display": 10,
            "sort": "date",
        }

        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        article = [
            {
                "title": item["title"],
                "link": item["link"],
                "description": item["description"],
                "pubDate": item["pubDate"],
            }
            for item in data.get("items", [])
        ]

        response_data = {
            "stock_code1": stock_code1,
            "stock_code2": stock_code2,
            "articles": article,
        }

        #return JsonResponse(response_data)
        return render(request, "ai/articles.html", response_data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)