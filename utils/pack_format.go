package utils

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
)

const MCMETA_REGISTRY = "https://raw.githubusercontent.com/misode/mcmeta/summary/versions/data.json"

type mcMetaRegistryItem struct {
	Id         string `json:"id"`
	PackFormat int    `json:"data_pack_version"`
}

func GetPackFormat(version string) int {
	cache := GetCache()

	if format, ok := cache.PackFormats[version]; ok {
		return format
	}

	response, err := http.Get(MCMETA_REGISTRY)
	if err != nil {
		log.Fatal(err)
	}

	defer response.Body.Close()
	responseBody, err := io.ReadAll(response.Body)
	if err != nil {
		log.Fatal(err.Error())
	}

	registry := []mcMetaRegistryItem{}
	err = json.Unmarshal(responseBody, &registry)
	if err != nil {
		log.Fatal(err)
	}

	for _, item := range registry {
		cache.PackFormats[item.Id] = item.PackFormat
	}

	SetCache(cache)

	format, ok := cache.PackFormats[version]
	if !ok {
		log.Fatalf("Pack format not found for version %s", version)
	}
	return format
}
