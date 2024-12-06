from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Stock, StockCorrelation
import requests
import FinanceDataReader as fdr
from django.http import JsonResponse

def price(request, stock_code):
    try:

        stock_df = fdr.DataReader(stock_code, '2023-06-01', '2024-07-26')

        latest_data = stock_df.iloc[-1]
        close_price = latest_data['Close']
        change_rate = latest_data['Change'] * 100

        dates = stock_df.index.strftime('%Y-%m-%d').tolist()
        close_prices = stock_df['Close'].tolist()

        response_data = {
            'stock_code': stock_code,
            'close_price': close_price,
            'change_rate': round(change_rate, 2),
            'dates': dates,
            'close_prices': close_prices,
        }

        return JsonResponse(response_data)

    except Exception as e:
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
        stock_code2 = "000150"
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

#(주식 종목, 코드) 반환 함수
def stock_list(request):
    try:
        krx_stocks = fdr.StockListing('KRX')

        stocks = krx_stocks[['Name', 'Symbol']].to_dict('records')

        '''
        위 코드 형식
        [
            {'Name': '삼성전자', 'Symbol': '005930'},
            {'Name': 'SK하이닉스', 'Symbol': '000660'},
            {'Name': '현대차', 'Symbol': '005380'}
            ...
        ]
        '''

        return JsonResponse({'status': 'success', 'stocks': stocks})

    except Exception as e:
        # 에러 처리
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
