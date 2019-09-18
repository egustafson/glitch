Operations
==========

(add _symbol_)        Add a new symbol
(activate _symbol_)   Activate / deactivate a symbol
(history _symbol_)    Symbol load history, splits, dividends
(indicators _symbol_) Symbol compute indicators (backfill)

(reset _symbol_)      Remove all history and indicator.
(pingdb)

(list)                List all symbols
(export _symbol_)     Export (CSV) a symbols history
?graph ??

(updateh)    Update history for active symbols
(updatei)    Update indicators for active symbols

----

Trade Tracking (Paper Trading)

Acount
 - id
 - Name
 - Fund(price, date)
 - Buy(sym, shares, price, fee, date)
 - Sell(sym, shares, price, fee, date)
 - Ballance() : dollars
 - Equities() : [ (sym, shares), ... ]
 - Fees() : total fees paid
 - Value(close date) : dollar value at close on date

Transaction
 - id
 - date
 - note
 - price   (+/-)
 - symbol
 - shares  (+/-)
 - fee
