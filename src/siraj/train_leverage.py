from agent.agent import Agent
from functions import *
import sys
from keras.models import load_model

window_size, episode_count = int(20), int(1000)

print("window_size:" + str(window_size))
print("episode_count:" + str(episode_count))

agent = Agent(window_size)
data = read_bitflyer_json()

length_data = len(data) - 1
batch_size = 50

try:
    model_name = sys.argv[1]
    model = load_model("models/" + model_name)
    agent = Agent(window_size, True, model_name)
    print("Model Loaded!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("=====================================================================")
except:
    import traceback

    traceback.print_exc()

for e in range(episode_count + 1):
    print("Episode " + str(e) + "/" + str(episode_count))
    state = getStateFromCsvData(data, 0, window_size)
    print(state)
    total_profit = 0
    agent.buy_inventory = []

    for idx in range(length_data):
        len_buy = len(agent.buy_inventory)
        len_sell = len(agent.sell_inventory)
        if len_buy > 40:
            buy_flag = 1
            sell_flag = 0
        elif len_sell > 40:
            buy_flag = 0
            sell_flag = 1
        else:
            buy_flag = 0
            sell_flag = 0

        buy_sell_array = [len_buy, len_sell, buy_flag, sell_flag]

        action = agent.act(state, buy_sell_array)

        # TODO idx + 1出なくて良いか？　バグの可能性あり。
        next_state = getStateFromCsvData(data, idx + 1, window_size)
        reward = 0

        if action == 1 and len(agent.sell_inventory) > 0:
            i = 0
            for i in range(0, int(len(agent.sell_inventory) / 10)):
                sold_price = agent.sell_inventory.pop(0)
                profit = sold_price - data[idx]
                reward += profit  # max(profit, 0)
                total_profit += profit
                print("Buy(決済): " + formatPrice(data[idx]) + " | Profit: " + formatPrice(profit))
            reward = reward / (i + 1)
        elif action == 1 and len(agent.buy_inventory) < 50:
            agent.buy_inventory.append(data[idx])
            print("Buy: " + formatPrice(data[idx]))
        elif action == 2 and len(agent.buy_inventory) > 0:
            i = 0
            for i in range(0, int(len(agent.buy_inventory) / 10)):
                bought_price = agent.buy_inventory.pop(0)
                profit = data[idx] - bought_price
                reward += profit  # max(profit, 0)
                total_profit += profit
                print("Sell: " + formatPrice(data[idx]) + " | Profit: " + formatPrice(profit))
            reward = reward / (i + 1)
        elif action == 2 and len(agent.sell_inventory) < 50:
            agent.sell_inventory.append(data[idx])
            print("Sell(空売り): " + formatPrice(data[idx]))

        print("inventory(sell) : " + str(len(agent.sell_inventory)))
        print("inventory(buy)  : " + str(len(agent.buy_inventory)))

        done = True if idx == length_data - 1 else False

        agent.memory.append((state, action, reward, next_state, done, buy_sell_array))
        state = next_state

        if idx % 10 == 0:
            print("--------------------------------")
            print("Total Profit: " + formatPrice(total_profit))
            print("--------------------------------")

        if len(agent.memory) > batch_size:
            agent.expReplay(batch_size)

    agent.model.save("models/model_ep" + str(e))
