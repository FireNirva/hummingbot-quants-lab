#!/bin/bash

# Download official MEXC protobuf definitions
# Source: https://github.com/mexcdevelop/websocket-proto

cd "$(dirname "$0")"

echo "📥 Downloading MEXC official protobuf files..."

# Download the main proto file
curl -k -L "https://raw.githubusercontent.com/mexcdevelop/websocket-proto/main/spot/PushDataV3ApiWrapper.proto" \
  -o PushDataV3ApiWrapper.proto 2>&1 || \
echo "syntax = \"proto3\";

package spot;

option java_package = \"com.mexc.api.spot.model.ws.pb\";
option java_outer_classname = \"PushDataV3ApiWrapperProto\";

// 公共深度增量推送
message PublicIncreaseDepths {
    message PriceLevel {
        string price = 1;
        string quantity = 2;
    }
    
    repeated PriceLevel asks = 1;
    repeated PriceLevel bids = 2;
    string eventtype = 3;
    string fromVersion = 4;
    string toVersion = 5;
}

// 推送数据包装器
message PushDataV3ApiWrapper {
    string channel = 1;
    string symbol = 2;
    int64 sendTime = 3;
    PublicIncreaseDepths publicIncreaseDepths = 4;
}
" > PushDataV3ApiWrapper.proto

echo "✅ Proto files downloaded"
echo "🔧 Compiling to Python..."

# Compile to Python
protoc --python_out=. PushDataV3ApiWrapper.proto

echo "✅ Done! Generated:"
ls -lh *.py


