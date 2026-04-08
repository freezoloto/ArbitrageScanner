import time
from scanner_exchanges import fetch_all_prices, find_arbitrage
from scanner_state import scanner_state


def scanner_loop(on_update_callback):
    while True:
        prices = fetch_all_prices()

        opps = find_arbitrage(
            prices,
            fee_mode=scanner_state.fee_mode
        )

        scanner_state.set_results(opps)
        on_update_callback(scanner_state.get_results())

        time.sleep(2)

