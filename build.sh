GOOS=linux GOARCH=amd64 go build -o dpm-linux_amd64
GOOS=darwin GOARCH=amd64 go build -o dpm-mac_amd64
GOOS=windows GOARCH=amd64 go build -o dpm-windows_amd64.exe