# Etapa 05.1 — Exemplos Práticos e Simulações Passo a Passo

> **Base Legal e Matemática:** Regras de apuração não cumulativa, alíquotas reduzidas e redutores sociais da Lei Complementar nº 214/2025.
> *(Nota: As alíquotas definitivas da CBS e do IBS serão fixadas por lei ordinária de cada ente após o período de calibragem; nos exemplos abaixo, utilizamos a alíquota de referência estimada pelo Ministério da Fazenda de **$26{,}5\%$** — sendo **$8{,}8\%$ de CBS** e **$17{,}7\%$ de IBS** — para demonstrar as fórmulas exatas).*

---

## Caso 1: Loja de Comércio Varejista (Descontando Créditos de Tudo!)

Imagine uma **Loja de Eletrodomésticos** que, em um mês, realiza as seguintes operações (valores líquidos, sem imposto):
* **Compras pagas no mês (Entradas com crédito):**
  - Compra de mercadorias da fábrica: $\text{R\$ } 100.000{,}00$
  - Aluguel da loja comercial (locador PJ no regime regular, alíquota reduzida em $70\% \Rightarrow 7{,}95\%$): $\text{R\$ } 10.000{,}00$
  - Energia elétrica e internet da loja: $\text{R\$ } 4.000{,}00$
  - Software ERP e agência de marketing: $\text{R\$ } 6.000{,}00$
* **Vendas realizadas no mês (Saídas):**
  - Venda de eletrodomésticos aos clientes: $\text{R\$ } 180.000{,}00$

### Memória de Cálculo e Desenho da Apuração

```text
+-----------------------------------------------------------------------------+
| 1. CRÉDITOS NAS COMPRAS DA LOJA (IMPOSTO PAGO NAS ENTRADAS)                 |
+-----------------------------------------------------------------------------+
| - Mercadorias: R$ 100.000,00 x 26,5% (8,8% CBS + 17,7% IBS) = R$ 26.500,00  |
| - Energia/Net: R$   4.000,00 x 26,5%                        = R$  1.060,00  |
| - ERP/Mkt:     R$   6.000,00 x 26,5%                        = R$  1.590,00  |
| - Aluguel*:    R$  10.000,00 x  7,95% (alíquota locação)    = R$    795,00  |
| --------------------------------------------------------------------------- |
| (=) TOTAL DE CRÉDITOS ACUMULADOS NO MÊS:                    = R$ 29.945,00  |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| 2. DÉBITOS NAS VENDAS DA LOJA (IMPOSTO DESTACADO NAS SAÍDAS)                |
+-----------------------------------------------------------------------------+
| - Vendas Líquidas: R$ 180.000,00                                            |
| - Débito de CBS (8,8%):  R$ 180.000,00 x 8,8%               = R$ 15.840,00  |
| - Débito de IBS (17,7%): R$ 180.000,00 x 17,7%              = R$ 31.860,00  |
| --------------------------------------------------------------------------- |
| (=) TOTAL DE DÉBITOS NAS VENDAS (Cobrado por fora na NF):   = R$ 47.700,00  |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| 3. SALDO A RECOLHER AO GOVERNO (DÉBITOS - CRÉDITOS)                         |
+-----------------------------------------------------------------------------+
|   R$ 47.700,00 (Débitos) - R$ 29.945,00 (Créditos) = R$ 17.755,00           |
|   (Alíquota efetiva desembolsada pela loja sobre a receita líquida = 9,86%) |
+-----------------------------------------------------------------------------+
```

---

## Caso 2: Prestador de Serviços B2B (Consultoria de TI / Engenharia)

Muita gente pensa: *"Minha empresa de engenharia/TI pagava 5% de ISS + 3,65% de PIS/COFINS = 8,65%. Agora vai para 26,5% (ou 18,55% com redução de 30%)! Vou quebrar?"*
**Veja a matemática completa quando o seu cliente é outra empresa (B2B):**

Suponha uma **Consultoria de TI** que vende um projeto para um **Banco ou Indústria** pelo preço total de contrato de $\text{R\$ } 10.000{,}00$ antes da reforma:

| Item | ANTES da Reforma (ISS 5% + PIS/COFINS 3,65% Cumulativo) | DEPOIS da Reforma (IVA Dual 26,5% "Por Fora") |
| :--- | :---: | :---: |
| **Preço cobrado na Nota Fiscal** | $\text{R\$ } 10.000{,}00$ | $\text{R\$ } 9.135{,}00 + \text{R\$ } 2.420{,}78\text{ (26,5\%)} = \text{R\$ } 11.555{,}78$ |
| **Imposto embutido / destacado** | $\text{R\$ } 865{,}00$ (por dentro) | $\text{R\$ } 2.420{,}78$ (por fora) |
| **Quanto sobra líquido para a Consultoria de TI?** | $10.000 - 865 = \mathbf{\text{R\$ } 9.135{,}00}$ | $\mathbf{\text{R\$ } 9.135{,}00}$ *(mais os créditos de computadores, nuvem e aluguel que ela passa a recuperar!)* |
| **Quanto o Cliente (Indústria) recupera de crédito?** | **$\text{R\$ } 0{,}00$** (ISS e PIS/COFINS cumulativo não davam crédito!) | **$\text{R\$ } 2.420{,}78$ (100% de crédito!)** |
| **Custo Real Líquido para o Cliente (Indústria):** | **$\text{R\$ } 10.000{,}00$** | $11.555{,}78 - 2.420{,}78 = \mathbf{\text{R\$ } 9.135{,}00}$ *(Ficou R$ 865,00 mais barato para o cliente!)* |

> **Lição de Ouro para Negócios B2B:** Na Reforma Tributária, ao negociar contratos entre empresas do regime regular, **negocie sempre o Preço Líquido (sem IBS/CBS)**, pois o imposto destacado "por fora" volta $100\%$ como crédito para o comprador!

---

## Caso 3: Compra de Imóvel Residencial Novo e Aluguel Residencial

Vamos aplicar as fórmulas oficiais da **LC 214/2025** para o setor imobiliário (supondo alíquota padrão de $26{,}5\%$):

### A) Compra de Apartamento Novo da Construtora por R$ 400.000,00
* **Dados:**
  - Preço de venda do apartamento: $\text{R\$ } 400.000{,}00$
  - Custo do terreno proporcional (Redutor de Ajuste): $\text{R\$ } 80.000{,}00$
  - Redutor Social de Habitação (LC 214/2025): $\text{R\$ } 100.000{,}00$
  - Alíquota do regime imobiliário (redução de $50\%$): $26{,}5\% \times 0{,}50 = \mathbf{13{,}25\%}$
* **Cálculo Passo a Passo:**
  $$\text{Base de Cálculo} = \text{Preço} - \text{Redutor de Ajuste} - \text{Redutor Social}$$
  $$\text{Base de Cálculo} = 400.000 - 80.000 - 100.000 = \mathbf{\text{R\$ } 220.000{,}00}$$
  $$\text{Tributo Bruto (Débito)} = 220.000 \times 13{,}25\% = \text{R\$ } 29.150{,}00$$
  - Como a construtora ainda **desconta os créditos** do cimento, aço, tijolos, projetos e serviços que comprou (suponha $\text{R\$ } 15.000{,}00$ de créditos), o imposto líquido pago pela construtora será de apenas:
    $$\text{IBS/CBS Líquido} = 29.150 - 15.000 = \mathbf{\text{R\$ } 14.150{,}00} \quad (\text{apenas } \mathbf{3{,}54\%} \text{ do valor do imóvel!})$$

### B) Aluguel Residencial de R$ 2.600,00/mês (Cobrado por Imobiliária/PJ Contribuinte)
* **Dados:**
  - Valor do aluguel mensal: $\text{R\$ } 2.600{,}00$
  - Redutor Social Mensal por imóvel residencial: $\text{R\$ } 600{,}00$
  - Alíquota de Locação (redução de $70\%$): $26{,}5\% \times (1 - 0{,}70) = \mathbf{7{,}95\%}$
* **Cálculo Passo a Passo:**
  $$\text{Base de Cálculo} = 2.600{,}00 - 600{,}00 = \mathbf{\text{R\$ } 2.000{,}00}$$
  $$\text{IBS + CBS devido} = 2.000{,}00 \times 7{,}95\% = \mathbf{\text{R\$ } 159{,}00}$$
  $$\text{Alíquota Efetiva sobre o Aluguel Total} = \frac{159{,}00}{2.600{,}00} = \mathbf{6{,}12\%}$$
  *(Lembrando: Se o proprietário for Pessoa Física com até 3 imóveis alugados ou receita de aluguel até $\text{R\$ } 240\text{ mil/ano}$, o IBS/CBS é **ZERO**!).*
