from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import sys
import datetime
import argparse

import backtrader as bt
import strategy
import reporter
import dataReader

modpath=os.path.dirname(os.path.abspath(sys.argv[0]))

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Backtesting Script'
        )
    )

    # todo: add strategy & understand config kwargs
    parser.add_argument('--ticker', required=True, nargs='+',
                        metavar='TICKER', help='ticker(s) to backtest')

    parser.add_argument('--fromdate', required=False, default='2001-01-01',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--todate', required=False, default=datetime.datetime.today().strftime('%Y-%m-%d'),
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')


    parser.add_argument('--initcash', required=False, type=int, default='3000000',
                        metavar='DOLLAR($)', help='cash you have at first')
    
    parser.add_argument('--commission', required=False, type=float, default='0.001',
                        metavar='PERCENT(%)', help='trade commission')

    parser.add_argument('--stake', required=False, type=int, default='1',
                        metavar='kwargs', help='kwargs in key=value format')
    
    parser.add_argument('--plot', required=False, default='',
                        nargs='?', const='{}',
                        metavar='kwargs', help='kwargs in key=value format')
    
    parser.add_argument('--strat', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--cerebro', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')
    
    parser.add_argument('--broker', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--sizer', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')


    return parser.parse_args(pargs)

def runtstrat(args=None):
    args = parse_args()
    
    # download data from internet
    dr=dataReader.StockDataReader(args.ticker)
    datas=dr.getStockValueData(args.fromdate, args.todate)

    # backtesting engine config
    cerebro = bt.Cerebro()
    for data in datas:
        cerebro.adddata(data)
    # for i, data in enumerate(datas):
    #     if i != 0:
    #         data.plotinfo.plotmaster = datas[0]
    #     cerebro.adddata(data)
    
    cerebro.broker.setcash(args.initcash)
    cerebro.broker.setcommission(args.commission)
    cerebro.addstrategy(strategy.SimpleSMA)
    # strats = cerebro.optstrategy(
    #     strategy.SimpleSMA,
    #     maperiod=range(10, 31)
    # )
    cerebro.addsizer(bt.sizers.FixedSize, stake=args.stake)

    analyzers = {
        'AnnualReturn': bt.analyzers.AnnualReturn,
        'Calmar': bt.analyzers.Calmar,
        'DrawDown': bt.analyzers.DrawDown,
        'TimeDrawDown': bt.analyzers.TimeDrawDown,
        'GrossLeverage': bt.analyzers.GrossLeverage,
        'PositionsValue': bt.analyzers.PositionsValue,
        'PyFolio': bt.analyzers.PyFolio,
        'LogReturnsRolling': bt.analyzers.LogReturnsRolling,
        'PeriodStats': bt.analyzers.PeriodStats,
        'Returns': bt.analyzers.Returns,
        'SharpeRatio': bt.analyzers.SharpeRatio,
        'SharpeRatio_A': bt.analyzers.SharpeRatio_A,
        'SQN': bt.analyzers.SQN,
        'TimeReturn': bt.analyzers.TimeReturn,
        'TradeAnalyzer': bt.analyzers.TradeAnalyzer,
        'Transactions': bt.analyzers.Transactions,
        'VWR': bt.analyzers.VWR,
    }
    
    for name, analyzer in analyzers.items():
        cerebro.addanalyzer(analyzer, _name=name)
    
    # resultFilePath = os.path.join(modpath, '../result/result.txt')
    # cerebro.addwriter(bt.WriterFile, out=resultFilePath, csv=True)

    results = cerebro.run()
    
    # report the analysis of backtesting
    analysis={name: results[0].analyzers.getbyname(name).get_analysis() for name in analyzers}
    reporter.report(args, analysis)

    cerebro.plot(style='candle', barup='red', bardown='blue')

if __name__ == '__main__':
    runtstrat()
