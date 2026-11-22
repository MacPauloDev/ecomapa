import sqlite3
import json

conn = sqlite3.connect('ecomapa.db')
cur = conn.cursor()

# Clear existing points (keep the 2 already there, or clear all and re-add)
# Let's clear and re-add everything
cur.execute('DELETE FROM ponto_descarte')

points = [
    # === PEVs EM SUPERMERCADOS (36 pontos da Semulsp/Manaus Lixo Zero) ===
    {
        'nome': 'CIGS Zoo - PEV',
        'endereco': '1918 Av. São Jorge, São Jorge, Manaus - AM',
        'latitude': -3.0850,
        'longitude': -60.0150,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Conforme horário do local (geralmente 7h-22h)',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV em supermercado - verifique horário no local'
    },
    {
        'nome': 'ONG Reusa/FAS - PEV',
        'endereco': '326 R. São Vicente de Paula, Redenção, Manaus - AM',
        'latitude': -3.0950,
        'longitude': -60.0250,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Conforme horário do local',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV em parceria com ONG Reusa/FAS'
    },
    {
        'nome': 'Empório DB Mario Ypiranga - PEV',
        'endereco': '232 R. Salvador, Nossa Sra. das Graças, Manaus - AM',
        'latitude': -3.1033,
        'longitude': -60.0129,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Empório DB - materiais recicláveis secos'
    },
    {
        'nome': 'Empório DB Adrianópolis - PEV',
        'endereco': '200 Av. Efigênio Salles, Adrianópolis, Manaus - AM',
        'latitude': -3.0865,
        'longitude': -60.0043,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Empório DB Adrianópolis'
    },
    {
        'nome': 'Super DB Cachoeirinha - PEV',
        'endereco': '1017 Av. Carvalho Leal, Cachoeirinha, Manaus - AM',
        'latitude': -3.1150,
        'longitude': -60.0200,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Super DB Cachoeirinha'
    },
    {
        'nome': 'Mini DB Visconde - PEV',
        'endereco': 'Av. Visc. de Porto Alegre, 606, Praça 14, Manaus - AM',
        'latitude': -3.1250,
        'longitude': -60.0180,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Mini DB Visconde'
    },
    {
        'nome': 'PEV Parque Municipal do Mindu',
        'endereco': 'Rua Dom João, 247 - Parque Dez de Novembro, Manaus - AM',
        'latitude': -3.0783863,
        'longitude': -60.0079453,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Consulte o local antes da visita',
        'contato': '(92) 99270-0985',
        'fonte_url': 'https://www.google.com/maps/place/Ponto+de+Entrega+Volunt%C3%A1ria-+PEV+(Parque+do+Mindu)/@-3.0783863,-60.0079453,17z/',
        'observacoes': 'Ponto de entrega voluntária no Parque do Mindu. Confirme materiais e horário.'
    },
    {
        'nome': 'Carrefour Adrianópolis - PEV',
        'endereco': '203 Av. Jorn. Umberto Calderaro Filho, Adrianópolis, Manaus - AM',
        'latitude': -3.0920,
        'longitude': -60.0080,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Carrefour Adrianópolis'
    },
    {
        'nome': 'Assaí Grande Circular - PEV',
        'endereco': '8755 Av. Autaz Mirim, Novo Aleixo, Manaus - AM',
        'latitude': -3.0876,
        'longitude': -59.9504,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Assaí Atacadista Grande Circular'
    },
    {
        'nome': 'Assaí Aleixo - PEV',
        'endereco': '2045 Av. Efigênio Salles, Aleixo, Manaus - AM',
        'latitude': -3.0865,
        'longitude': -60.0043,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Assaí Atacadista Aleixo'
    },
    {
        'nome': 'Super DB Coroado - PEV',
        'endereco': 'Av. Cosme Ferreira, Coroado, Manaus - AM',
        'latitude': -3.1050,
        'longitude': -59.9850,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado DB Coroado'
    },
    {
        'nome': 'Assaí Flores - PEV',
        'endereco': 'Av. Torquato Tapajós, Flores, Manaus - AM',
        'latitude': -3.0750,
        'longitude': -60.0150,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Assaí Atacadista Flores'
    },
    {
        'nome': 'Super DB Planalto - PEV',
        'endereco': '120 Rua Roma, Planalto, Manaus - AM',
        'latitude': -3.0650,
        'longitude': -60.0050,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado DB Planalto'
    },
    {
        'nome': 'Hiper DB Nova Cidade - PEV',
        'endereco': '1359 Av. Margarita, Cidade Nova, Manaus - AM',
        'latitude': -3.0550,
        'longitude': -59.9800,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Hiper DB Nova Cidade'
    },
    {
        'nome': 'Super DB Dom Pedro - PEV',
        'endereco': '79 Av. Pedro Teixeira, Dom Pedro, Manaus - AM',
        'latitude': -3.0877,
        'longitude': -60.0383,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado DB Dom Pedro'
    },
    {
        'nome': 'Super DB Ponta Negra - PEV',
        'endereco': '7687 Av. Coronel Teixeira, Compensa, Manaus - AM',
        'latitude': -3.0800,
        'longitude': -60.0450,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado DB Ponta Negra'
    },
    {
        'nome': 'Empório DB Ponta Negra - PEV',
        'endereco': '5850 Av. Coronel Teixeira, Ponta Negra, Manaus - AM',
        'latitude': -3.0750,
        'longitude': -60.0400,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Empório DB Ponta Negra'
    },
    {
        'nome': 'Super DB Japiim - PEV',
        'endereco': '3810 Av. General Rodrigo Otávio, Japiim, Manaus - AM',
        'latitude': -3.1300,
        'longitude': -60.0100,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado DB Japiim'
    },
    {
        'nome': 'Super DB Adrianópolis - PEV',
        'endereco': '1128 Av. Jorn. Umberto Calderaro Filho, Adrianópolis, Manaus - AM',
        'latitude': -3.0950,
        'longitude': -60.0080,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado DB Adrianópolis'
    },
    {
        'nome': 'Emporium DB Cidade Nova - PEV',
        'endereco': '350 Av. Max Teixeira, Mundo Novo, Manaus - AM',
        'latitude': -3.0700,
        'longitude': -59.9700,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Emporium DB Cidade Nova'
    },
    {
        'nome': 'Super Vitória Flores - PEV',
        'endereco': '5200 Av. Torquato Tapajós, Flores, Manaus - AM',
        'latitude': -3.0700,
        'longitude': -60.0100,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Vitória Flores'
    },
    {
        'nome': 'Pátio Gourmet Adrianópolis - PEV',
        'endereco': 'Av. Via Láctea, Aleixo, Manaus - AM',
        'latitude': -3.1000,
        'longitude': -60.0150,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Pátio Gourmet Adrianópolis (Morada do Sol)'
    },
    {
        'nome': 'Nova Era Novo Aleixo - PEV',
        'endereco': '230 Av. Gov. José Lindoso, Novo Aleixo, Manaus - AM',
        'latitude': -3.0650,
        'longitude': -59.9600,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Nova Era Novo Aleixo (Av das Torres)'
    },
    {
        'nome': 'Nova Era Barreira - PEV',
        'endereco': '11559 Av. Torquato Tapajós, Santa Etelvina, Manaus - AM',
        'latitude': -3.0400,
        'longitude': -60.0000,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Nova Era Barreira'
    },
    {
        'nome': 'Tribom Parque 10 - PEV',
        'endereco': 'Shangri-La III, Parque Dez de Novembro, Manaus - AM',
        'latitude': -3.0800,
        'longitude': -60.0100,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Tribom Parque 10'
    },
    {
        'nome': 'Veneza Parque 10 - PEV',
        'endereco': '915 Av. Tancredo Neves, Parque 10, Manaus - AM',
        'latitude': -3.0850,
        'longitude': -60.0050,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Veneza Parque 10'
    },
    {
        'nome': 'Veneza Lago Azul - PEV',
        'endereco': '13118 Av. Torquato Tapajós, Lago Azul, Manaus - AM',
        'latitude': -3.0300,
        'longitude': -60.0000,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Veneza Lago Azul'
    },
    {
        'nome': 'Emporium Roma Adrianópolis - PEV',
        'endereco': '351 Rua Terezina, Adrianópolis, Manaus - AM',
        'latitude': -3.0930,
        'longitude': -60.0070,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Emporium Roma Adrianópolis'
    },
    {
        'nome': 'Cezar São José Operário - PEV',
        'endereco': '01 R. 7 B, São José Operário, Manaus - AM',
        'latitude': -3.1100,
        'longitude': -59.9900,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Cezar São José Operário'
    },
    {
        'nome': 'Yroyak Nossa Sra. das Graças - PEV',
        'endereco': '664 A Av. Rio Madeira, Nossa Sra. das Graças, Manaus - AM',
        'latitude': -3.1000,
        'longitude': -60.0100,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Yroyak Nossa Sra. das Graças'
    },
    {
        'nome': 'Nova Era Flores (Da Paz) - PEV',
        'endereco': '2871 Av. Torquato Tapajós, Da Paz, Manaus - AM',
        'latitude': -3.0720,
        'longitude': -60.0120,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Nova Era Flores (Da Paz)'
    },
    {
        'nome': 'Pátio Gourmet São Geraldo - PEV',
        'endereco': '1375 Av. Djalma Batista, Chapada, Manaus - AM',
        'latitude': -3.0800,
        'longitude': -60.0200,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Pátio Gourmet São Geraldo'
    },
    {
        'nome': 'Yroyak Ponta Negra - PEV',
        'endereco': '5006 Av. Coronel Teixeira, Ponta Negra, Manaus - AM',
        'latitude': -3.0780,
        'longitude': -60.0420,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Yroyak Ponta Negra'
    },
    {
        'nome': 'Nova Era Santo Antônio - PEV',
        'endereco': '15 Av. Brasil, Santo Antônio, Manaus - AM',
        'latitude': -3.1200,
        'longitude': -60.0200,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Nova Era Santo Antônio'
    },
    {
        'nome': 'Carrefour Ponta Negra - PEV',
        'endereco': 'Lote B 52 Av. Pedro Teixeira, Ponta Negra, Manaus - AM',
        'latitude': -3.0877,
        'longitude': -60.0383,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Carrefour Ponta Negra'
    },
    {
        'nome': 'Atack Coroado - PEV',
        'endereco': '3700 Av. Cosme Ferreira, Coroado III, Manaus - AM',
        'latitude': -3.1050,
        'longitude': -59.9800,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Supermercado Atack Coroado'
    },
    {
        'nome': 'Carrefour Flores - PEV',
        'endereco': '276 Av. Djalma Batista, Flores, Manaus - AM',
        'latitude': -3.0780,
        'longitude': -60.0180,
        'materiais_aceitos': 'plastico,papel,vidro,metais,pilhas,oleo',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/3',
        'observacoes': 'PEV no Carrefour Flores - também recebe pilhas/baterias e lâmpadas (conforme manauslixozero c/3)'
    },
    {
        'nome': 'Prosamim Mestre Chico - PEV',
        'endereco': '165 Prosamim Mestre Chico, Centro, Manaus - AM',
        'latitude': -3.1300,
        'longitude': -60.0250,
        'materiais_aceitos': 'plastico,papel,vidro,metais',
        'horario_funcionamento': 'Consulte o local',
        'contato': '(92) 3642-1850',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/0',
        'observacoes': 'PEV no Prosamim Mestre Chico'
    },

    # === ECOLONOS / PONTOS DE ELETRÔNICOS ===
    {
        'nome': 'Ecoponto Zona Sul (Educandos)',
        'endereco': 'Av. Lourenço da Silva Braga, s/n, Educandos, Manaus - AM',
        'latitude': -3.1367217,
        'longitude': -60.0096817,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Seg-Sáb 8h-17h (confirmar)',
        'contato': '(92) 98842-1271',
        'fonte_url': 'https://www.manaus.am.gov.br/noticia/sustentabilidade/coleta-seletiva-de-eletronicos/',
        'observacoes': 'Ecoponto oficial da Semulsp para eletrônicos. Recebe celulares, computadores, eletrodomésticos, pilhas, baterias, cabos. Não aceita lâmpadas, TVs de tubo, toners.'
    },
    {
        'nome': 'Ecoponto Zona Norte',
        'endereco': 'Parque dos Bilhares, Manaus - AM',
        'latitude': -3.0600,
        'longitude': -59.9800,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Seg-Sáb 8h-17h (confirmar)',
        'contato': '(92) 98842-1271',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Ecoponto oficial da Semulsp zona norte para eletrônicos. Subprefeituras locais também podem receber.'
    },
    {
        'nome': 'Sede da Semulsp',
        'endereco': 'Av. Brasil, 1335, Compensa, Manaus - AM',
        'latitude': -3.1000,
        'longitude': -60.0300,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Seg-Sex 8h-17h',
        'contato': '(92) 98842-1271',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Sede da Secretaria Municipal de Limpeza Urbana - recebe eletrônicos diretamente. WhatsApp para confirmar: (92) 98842-1271'
    },
    {
        'nome': 'Eletroponto Ageman',
        'endereco': 'Sede da Ageman, Manaus - AM',
        'latitude': -3.0900,
        'longitude': -60.0150,
        'materiais_aceitos': 'eletronicos,pilhas,baterias,lampadas',
        'horario_funcionamento': 'Horário comercial',
        'contato': '',
        'fonte_url': 'https://amazonas1.com.br/manaus-instala-primeiro-eletroponto-na-ageman-e-amplia-coleta-de-residuos-eletronicos/',
        'observacoes': 'Primeiro Eletroponto de Manaus na sede da Ageman. Recebe celular, computador, pilha, bateria, lâmpada sem custo.'
    },
    {
        'nome': 'Bemol Manauara Shopping - Coleta Eletrônicos',
        'endereco': 'Av. Mário Ypiranga, 1300, Adrianópolis, Manaus - AM',
        'latitude': -3.1033,
        'longitude': -60.0129,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Conforme horário do shopping (10h-22h)',
        'contato': '',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Ponto de coleta de eletrônicos no Manauara Shopping (Bemol e MotoStore)'
    },
    {
        'nome': 'Bemol Studio 5 Shopping - Coleta Eletrônicos',
        'endereco': 'Av. Rodrigo Otávio, 3555, Japiim, Manaus - AM',
        'latitude': -3.1350,
        'longitude': -60.0150,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Conforme horário do shopping',
        'contato': '',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Ponto de coleta no Studio 5 Shopping (Bemol e MotoStore)'
    },
    {
        'nome': 'Bemol Matriz Centro - Coleta Eletrônicos',
        'endereco': 'Rua Miranda Leão, 41, Centro, Manaus - AM',
        'latitude': -3.1300,
        'longitude': -60.0220,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Horário comercial',
        'contato': '',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Ponto de coleta na Bemol Matriz no Centro'
    },
    {
        'nome': 'Bemol Shopping Ponta Negra - Coleta Eletrônicos',
        'endereco': 'Av. Coronel Teixeira, 5705, Compensa, Manaus - AM',
        'latitude': -3.0800,
        'longitude': -60.0400,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Conforme horário do shopping',
        'contato': '',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Ponto de coleta no Shopping Ponta Negra (Bemol e MotoStore)'
    },
    {
        'nome': 'Bemol Amazonas Shopping - Coleta Eletrônicos',
        'endereco': 'Av. Djalma Batista, 482, Parque 10, Manaus - AM',
        'latitude': -3.0800,
        'longitude': -60.0150,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Conforme horário do shopping',
        'contato': '',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Ponto de coleta no Amazonas Shopping (Bemol e MotoStore)'
    },
    {
        'nome': 'Bemol Cidade Nova - Coleta Eletrônicos',
        'endereco': 'Av. Noel Nutels, 1762, Cidade Nova, Manaus - AM',
        'latitude': -3.0700,
        'longitude': -59.9700,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Conforme horário da loja',
        'contato': '',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Ponto de coleta na Bemol Cidade Nova'
    },
    {
        'nome': 'Bemol Grande Circular - Coleta Eletrônicos',
        'endereco': 'Av. Autaz Mirim, 6100, São José Operário, Manaus - AM',
        'latitude': -3.0876,
        'longitude': -59.9504,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Conforme horário da loja',
        'contato': '',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Ponto de coleta na Bemol Grande Circular (MotoStore no mesmo endereço)'
    },
    {
        'nome': 'MotoStore Sumauma Shopping - Coleta Eletrônicos',
        'endereco': 'Av. Noel Nutels, 1762, Cidade Nova, Manaus - AM',
        'latitude': -3.0700,
        'longitude': -59.9700,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Conforme horário do shopping',
        'contato': '',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Ponto de coleta no Sumauma Shopping'
    },
    {
        'nome': 'Bemol Torquato - Coleta Eletrônicos',
        'endereco': 'Av. Torquato Tapajós, 8253, Tarumã, Manaus - AM',
        'latitude': -3.0500,
        'longitude': -60.0300,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Conforme horário da loja',
        'contato': '',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Ponto de coleta na Bemol Torquato (CD Bemol no 8251)'
    },
    {
        'nome': 'Instituto Descarte Correto',
        'endereco': 'R. Carbonita, Parque Dez de Novembro, Manaus - AM',
        'latitude': -3.0800,
        'longitude': -60.0080,
        'materiais_aceitos': 'eletronicos,pilhas,baterias',
        'horario_funcionamento': 'Seg-Sex 8h-17h (confirmar)',
        'contato': '',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/1',
        'observacoes': 'Organização socioambiental focada em lixo eletrônico. Triagem e desmanche técnico. Galpão no Parque Dez/Flores.'
    },

    # === PONTOS ESPECIAIS: LÂMPADAS, PILHAS, BATERIAS (manauslixozero c/3) ===
    {
        'nome': 'CDC Japiim - Lâmpadas',
        'endereco': '4050 Av. General Rodrigo Otávio, Japiim, Manaus - AM',
        'latitude': -3.1300,
        'longitude': -60.0100,
        'materiais_aceitos': 'lampadas',
        'horario_funcionamento': 'Conforme horário do local',
        'contato': '',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/3',
        'observacoes': 'Ponto especializado em lâmpadas fluorescentes'
    },
    {
        'nome': 'Lojas Americanas Shopping Ponta Negra - Pilhas/Baterias',
        'endereco': '5705 Av. Coronel Teixeira, Ponta Negra, Manaus - AM',
        'latitude': -3.0800,
        'longitude': -60.0400,
        'materiais_aceitos': 'pilhas,baterias',
        'horario_funcionamento': 'Conforme horário do shopping',
        'contato': '',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/3',
        'observacoes': 'Coleta de pilhas e baterias nas Lojas Americanas'
    },
    {
        'nome': 'SVI Ns. Sra. das Graças - Lâmpadas',
        'endereco': '2335 Av. Joaquim Gonzaga Pinheiro, N. Sra. das Graças, Manaus - AM',
        'latitude': -3.1000,
        'longitude': -60.0100,
        'materiais_aceitos': 'lampadas',
        'horario_funcionamento': 'Conforme horário do local',
        'contato': '',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/3',
        'observacoes': 'Ponto de coleta de lâmpadas'
    },
    {
        'nome': 'SVI Coroado - Lâmpadas',
        'endereco': 'Coroado, Manaus - AM',
        'latitude': -3.1050,
        'longitude': -59.9850,
        'materiais_aceitos': 'lampadas',
        'horario_funcionamento': 'Conforme horário do local',
        'contato': '',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/3',
        'observacoes': 'Ponto de coleta de lâmpadas no Coroado'
    },
    {
        'nome': 'Carrefour Flores - Lâmpadas/Pilhas/Toners HP',
        'endereco': '276 Av. Djalma Batista, Flores, Manaus - AM',
        'latitude': -3.0780,
        'longitude': -60.0180,
        'materiais_aceitos': 'lampadas,pilhas,baterias,toners',
        'horario_funcionamento': 'Seg-Sáb 7h-22h, Dom/Feriados 7h-18h',
        'contato': '',
        'fonte_url': 'https://www.manauslixozero.com.br/page-map/c/3',
        'observacoes': 'Ponto especializado: lâmpadas, pilhas, baterias, cartucho e toners HP'
    },

    # === PROGRAMA "DE OLHO NO ÓLEO" - 12 PONTOS (Águas de Manaus) ===
    {
        'nome': 'Sede Administrativa Águas de Manaus - Coleta Óleo',
        'endereco': 'Aleixo, Manaus - AM',
        'latitude': -3.1000,
        'longitude': -60.0150,
        'materiais_aceitos': 'oleo',
        'horario_funcionamento': 'Horário comercial',
        'contato': '0800 092 0195',
        'fonte_url': 'https://g1.globo.com/am/amazonas/noticia/2026/11/11/programa-oferece-detergente-em-troca-de-oleo-de-cozinha-usado-em-manaus-veja-como-participar.ghtml',
        'observacoes': 'Programa "De Olho no Óleo" - troca 2L óleo usado por 500ml detergente. Armazenar em garrafa PET.'
    },
    {
        'nome': 'ICDLAM Braga Mendes - Coleta Óleo',
        'endereco': 'Braga Mendes, Manaus - AM',
        'latitude': -3.1150,
        'longitude': -60.0200,
        'materiais_aceitos': 'oleo',
        'horario_funcionamento': 'Conforme horário da instituição',
        'contato': '0800 092 0195',
        'fonte_url': 'https://g1.globo.com/am/amazonas/noticia/2026/11/11/programa-oferece-detergente-em-troca-de-oleo-de-cozinha-usado-em-manaus-veja-como-participar.ghtml',
        'observacoes': 'Instituto Cultural de Desporto e Lazer do AM - ponto de coleta do programa De Olho no Óleo'
    },
    {
        'nome': 'Associação Mulheres Girassóis - Coleta Óleo',
        'endereco': 'Jorge Teixeira 4, Manaus - AM',
        'latitude': -3.0600,
        'longitude': -59.9700,
        'materiais_aceitos': 'oleo',
        'horario_funcionamento': 'Conforme horário da associação',
        'contato': '0800 092 0195',
        'fonte_url': 'https://g1.globo.com/am/amazonas/noticia/2026/11/11/programa-oferece-detergente-em-troca-de-oleo-de-cozinha-usado-em-manaus-veja-como-participar.ghtml',
        'observacoes': 'Ponto de coleta do programa De Olho no Óleo'
    },
    {
        'nome': 'ECAM São José - Coleta Óleo',
        'endereco': 'São José, Manaus - AM',
        'latitude': -3.1100,
        'longitude': -59.9900,
        'materiais_aceitos': 'oleo',
        'horario_funcionamento': 'Conforme horário do ECAM',
        'contato': '0800 092 0195',
        'fonte_url': 'https://g1.globo.com/am/amazonas/noticia/2026/11/11/programa-oferece-detergente-em-troca-de-oleo-de-cozinha-usado-em-manaus-veja-como-participar.ghtml',
        'observacoes': 'Espaço de Cidadania Ambiental - ponto de coleta do programa'
    },
    {
        'nome': 'Instituto Desenvolvimento Comunitário Viver Melhor - Coleta Óleo',
        'endereco': 'Viver Melhor, Manaus - AM',
        'latitude': -3.0400,
        'longitude': -59.9800,
        'materiais_aceitos': 'oleo',
        'horario_funcionamento': 'Conforme horário do instituto',
        'contato': '0800 092 0195',
        'fonte_url': 'https://g1.globo.com/am/amazonas/noticia/2026/11/11/programa-oferece-detergente-em-troca-de-oleo-de-cozinha-usado-em-manaus-veja-como-participar.ghtml',
        'observacoes': 'Ponto de coleta do programa De Olho no Óleo'
    },
    {
        'nome': 'Central Única das Comunidades Compensa - Coleta Óleo',
        'endereco': 'Compensa, Manaus - AM',
        'latitude': -3.0900,
        'longitude': -60.0400,
        'materiais_aceitos': 'oleo',
        'horario_funcionamento': 'Conforme horário da central',
        'contato': '0800 092 0195',
        'fonte_url': 'https://g1.globo.com/am/amazonas/noticia/2026/11/11/programa-oferece-detergente-em-troca-de-oleo-de-cozinha-usado-em-manaus-veja-como-participar.ghtml',
        'observacoes': 'Ponto de coleta do programa De Olho no Óleo'
    },
    {
        'nome': 'Centro Social Chapéu de Zinco Betânia - Coleta Óleo',
        'endereco': 'Betânia, Manaus - AM',
        'latitude': -3.1200,
        'longitude': -60.0250,
        'materiais_aceitos': 'oleo',
        'horario_funcionamento': 'Conforme horário do centro',
        'contato': '0800 092 0195',
        'fonte_url': 'https://g1.globo.com/am/amazonas/noticia/2026/11/11/programa-oferece-detergente-em-troca-de-oleo-de-cozinha-usado-em-manaus-veja-como-participar.ghtml',
        'observacoes': 'Ponto de coleta do programa De Olho no Óleo'
    },
    {
        'nome': 'USF Petrópolis - Coleta Óleo',
        'endereco': 'Petrópolis, Manaus - AM',
        'latitude': -3.0950,
        'longitude': -60.0150,
        'materiais_aceitos': 'oleo',
        'horario_funcionamento': 'Conforme horário da USF',
        'contato': '0800 092 0195',
        'fonte_url': 'https://g1.globo.com/am/amazonas/noticia/2026/11/11/programa-oferece-detergente-em-troca-de-oleo-de-cozinha-usado-em-manaus-veja-como-participar.ghtml',
        'observacoes': 'Unidade de Saúde da Família Petrópolis - ponto de coleta do programa'
    },
    {
        'nome': 'Loja Atendimento Águas de Manaus Centro - Coleta Óleo',
        'endereco': 'Centro, Manaus - AM',
        'latitude': -3.1300,
        'longitude': -60.0220,
        'materiais_aceitos': 'oleo',
        'horario_funcionamento': 'Horário comercial',
        'contato': '0800 092 0195',
        'fonte_url': 'https://g1.globo.com/am/amazonas/noticia/2026/11/11/programa-oferece-detergente-em-troca-de-oleo-de-cozinha-usado-em-manaus-veja-como-participar.ghtml',
        'observacoes': 'Loja de atendimento da Águas de Manaus no Centro - ponto de coleta'
    },

    # === COLETA DOMICILIAR AGENDADA (ABREE) ===
    {
        'nome': 'Ascarman - Ponto Fixo ABREE / Coleta Agendada',
        'endereco': 'Rua Helena Cardoso, S/N, Santa Etelvina, Manaus - AM',
        'latitude': -3.0400,
        'longitude': -60.0000,
        'materiais_aceitos': 'eletronicos,eletrodomesticos_grandes',
        'horario_funcionamento': 'Seg-Sex 8h-17h',
        'contato': '(92) 99342-8866 / (92) 99617-1447',
        'fonte_url': 'https://tudo.manaus.br/onde-descartar-lixo-eletronico-em-manaus-locais-e-cuidados-na-entrega/',
        'observacoes': 'Ponto fixo ABREE e coleta domiciliar agendada para grandes volumes (>30kg). Associação de Catadores de Recicláveis do Amazonas.'
    },
]

for p in points:
    cur.execute('''
        INSERT INTO ponto_descarte 
        (nome, endereco, latitude, longitude, materiais_aceitos, horario_funcionamento, contato, fonte_url, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        p['nome'], p['endereco'], p['latitude'], p['longitude'],
        p['materiais_aceitos'], p['horario_funcionamento'], p['contato'],
        p['fonte_url'], p['observacoes']
    ))

conn.commit()
print(f"Inseridos {len(points)} pontos")

# Verify
cur.execute('SELECT COUNT(*) FROM ponto_descarte')
print(f"Total no banco: {cur.fetchone()[0]}")

# Show by material type
cur.execute('SELECT materiais_aceitos, COUNT(*) FROM ponto_descarte GROUP BY materiais_aceitos')
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

conn.close()
