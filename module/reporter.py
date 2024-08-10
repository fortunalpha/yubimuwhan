import pprint
from datetime import datetime
from tabulate import tabulate

def calc_avg(data: dict) -> float:
    total: float = 0
    i: int = 0
    
    for _, val in data.items():
        if isinstance(val, (int, float)):
            total += val
            i += 1
    
    return total / i
        
def process_analysis(analysis: dict):
    result = {}
    ndigit = 2

    for analyzer, data in analysis.items():
        if analyzer == 'TradeAnalyzer':
            result.setdefault('Total Trade', data.get('total').get('total'))
            result.setdefault('Total Gross', round(data.get('pnl').get('gross').get('total'), ndigit))
            result.setdefault('Avg. Gross', round(data.get('pnl').get('gross').get('average'), ndigit))
            result.setdefault('Total Net', round(data.get('pnl').get('net').get('total'), ndigit))
            result.setdefault('Avg. Net', round(data.get('pnl').get('net').get('average'), ndigit))
            
            win_rate = 100 * round(float(data.get('won').get('total')) / float(result.get('Total Trade')), ndigit)
            result.setdefault('Win Rate [%]', win_rate)

        # contained in PeriodStats
        elif analyzer == 'AnnualReturn':
            # Yearly Return [%] = (Final Value - Start Value) / Start Value * 100
            # avg = calc_avg(data)
            # result.setdefault('Avg. Returns (ann.) [%]', round(avg * 100, ndigit))
            pass        

        elif analyzer == 'Calmar':
            # Calmar ratio = Average Annual Rate of Return / Maximum Drawdown.
            avg = calc_avg(data)
            result.setdefault('Avg. Calmar ratio', round(avg, ndigit))
            
        elif analyzer == 'DrawDown':
            result.setdefault('Avg. DrawDown [%]', round(data.get('drawdown'), ndigit))
            # result.setdefault('DrawDown Length [Day]', data.get('len'))
            # result.setdefault('Money Down [$]', round(data.get('moneydown'), ndigit))
            result.setdefault('Max. Drawdown [%]', round(data.get('max').get('drawdown'), ndigit))
            # result.setdefault('Max. Drawdown Money Down', data.get('max').get('maxdrawdownperiod'))

        elif analyzer == 'TimeDrawDown':
            pass

        elif analyzer == 'GrossLeverage':
            pass
        
        elif analyzer == 'PositionsValue':
            pass
        
        elif analyzer == 'PyFolio':
            pass
        
        elif analyzer == 'LogReturnsRolling':
            pass
        
        elif analyzer == 'PeriodStats':
            result.setdefault('Avg. Returns (ann.) [%]', round(data.get('average'), ndigit))
            result.setdefault('Best Returns (ann.) [%]', round(data.get('best'), ndigit))
            result.setdefault('Worst Returns (ann.) [%]', round(data.get('worst'), ndigit))

        elif analyzer == 'Returns':
            result.setdefault('Total Returns [%]', round(data.get('rtot'), ndigit))
        
        elif analyzer == 'SharpeRatio':
            result.setdefault('Sharpe Ratio', round(data.get('sharperatio'), ndigit))
        
        elif analyzer == 'SharpeRatio_A':
            pass
        
        elif analyzer == 'SQN':
            result.setdefault('SQN', round(data.get('sqn'), ndigit))
        
        elif analyzer == 'TimeReturn':
            pass
        
        elif analyzer == 'Transactions':
            pass
        
        elif analyzer == 'VWR':
            pass
        
    return result

def report_result(result_dict: dict):
    for k, v in result_dict.items():
        print("{:<25}".format(k), end="")
        print("{:>25}".format(v))

def report(args, analysis: dict):
    result_dict = {}
    
    result_dict.setdefault('Start Date', args.fromdate)
    result_dict.setdefault('End Date', args.todate)
    duration = str(datetime.strptime(args.todate, '%Y-%M-%d') - datetime.strptime(args.fromdate, '%Y-%M-%d'))
    result_dict.setdefault('Duration', duration)
    # result_dict.setdefault('Strategy', args.strat)
    
    result_dict.update(process_analysis(analysis))
        
    report_result(result_dict)
    