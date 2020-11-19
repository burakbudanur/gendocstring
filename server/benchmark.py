# Copyright 2020-present Tae Hwan Jung
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import argparse
import requests
from tqdm import tqdm

def main(args):
    data = {'code': ('a = 1000 * b + 1000 * c + 1000 * b + 1000 * c + 1000 * b + 1000 * c ' * 100).strip()}
    headers = {'Content-Type': 'application/json;'}
    times = []
    for _ in tqdm(range(args.trials)):
        response = requests.post(
            f'http://{args.host}:{args.port}/summary',
            data=json.dumps(data),
            headers=headers,
        )
        assert response.status_code == 200
        response = json.loads(response.text)
        times.append(float(response['time']))

    print(sum(times) / len(times))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--host", type=str, default='127.0.0.1')
    parser.add_argument("--port", type=int, default=5000)

    args = parser.parse_args()

    main(args)