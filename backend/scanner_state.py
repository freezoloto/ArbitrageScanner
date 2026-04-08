class ScannerState:
    def __init__(self):
        self.results = []
        self.min_spread = 0.0
        self.fee_mode = "taker"  # taker / maker_taker / both
        self.enabled_exchanges = []  # пусто = все биржи
        self.enabled_pairs = []      # пусто = все пары
        self.sort_field = "net_spread"
        self.sort_desc = True

    def set_results(self, results):
        # фильтруем по биржам
        if self.enabled_exchanges:
            results = [
                r for r in results
                if r["buy_exchange"] in self.enabled_exchanges
                and r["sell_exchange"] in self.enabled_exchanges
            ]

        # фильтруем по парам
        if self.enabled_pairs:
            results = [r for r in results if r["pair"] in self.enabled_pairs]

        # фильтр по минимальному спреду
        results = [
            r for r in results
            if r.get("net_spread", 0) >= self.min_spread
        ]

        # сортировка
        results = sorted(
            results,
            key=lambda x: x.get(self.sort_field, 0),
            reverse=self.sort_desc
        )

        self.results = results

    def get_results(self):
        return self.results

    def set_min_spread(self, value):
        try:
            self.min_spread = float(value)
        except:
            self.min_spread = 0.0

    def set_fee_mode(self, mode):
        if mode in ["taker", "maker_taker", "both"]:
            self.fee_mode = mode

    def set_enabled_exchanges(self, lst):
        self.enabled_exchanges = lst

    def set_enabled_pairs(self, lst):
        self.enabled_pairs = lst

    def set_sort(self, field, desc):
        self.sort_field = field
        self.sort_desc = bool(desc)


scanner_state = ScannerState()

