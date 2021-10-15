import pandas_datareader as web

ativos_label = ["ABEV3.SA", "B3SA3.SA","BBSE3.SA", "BRML3.SA", "BBDC3.SA", "BBDC4.SA","BRAP4.SA","BBAS3.SA","BRKM5.SA","BRFS3.SA", "CCRO3.SA","CMIG4.SA","CIEL3.SA","COGN3.SA","CSAN3.SA","CVCB3.SA","CYRE3.SA","ECOR3.SA","ELET3.SA","ELET6.SA","EMBR3.SA","ENBR3.SA","EGIE3.SA","EQTL3.SA","FLRY3.SA","GGBR4.SA","GOAU4.SA","GOLL4.SA","HYPE3.SA","IGTA3.SA","ITSA4.SA","ITUB4.SA","JBSS3.SA","KLBN11.SA","RENT3.SA","LAME4.SA","LREN3.SA","MGLU3.SA","MRFG3.SA","MRVE3.SA","MULT3.SA","PETR3.SA","PETR4.SA","QUAL3.SA","RADL3.SA","SBSP3.SA","SANB11.SA","CSNA3.SA","SULA11.SA","TAEE11.SA","VIVT3.SA","TOTS3.SA","UGPA3.SA","USIM5.SA","VALE3.SA","WEGE3.SA","YDUQ3.SA","^BVSP"]

ativos_cotacoes = []
for ativo_label in ativos_label:
  print("taking " + ativo_label + " data")
  web.DataReader(ativo_label, data_source='yahoo', start='2015-01-01', end='2019-12-31').to_csv(ativo_label + '.csv')
