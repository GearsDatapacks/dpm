package alias

import (
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/gearsdatapacks/dpm/settings"
	"github.com/gearsdatapacks/dpm/types"
	"github.com/gearsdatapacks/dpm/utils"
)

func CreateAlias(context types.Context) {
	if _, err := os.ReadDir(settings.DpmDir); err != nil {
		err := os.Mkdir(settings.DpmDir, 0777)
		if err != nil {
			log.Fatal(err)
		}
	}

	if !utils.Exists(utils.AliasFile) {
		_, err := os.Create(utils.AliasFile)
		if err != nil {
			log.Fatal(err)
		}
	}

	contents, err := os.ReadFile(utils.AliasFile)
	if err != nil {
		log.Fatal(err)
	}

	aliases := map[string]string{}
	json.Unmarshal(contents, &aliases)

	name, auth := context.Values[0], context.Values[1]

	aliases[name] = auth

	setAliases(aliases)

	fmt.Printf("Created alias %q\n", name)
}

func RemoveAlias(context types.Context) {
	name := context.Values[0]

	if !utils.Exists(utils.AliasFile) {
		fmt.Printf("Alias %q does not exist\n", name)
		return
	}
	aliases := GetAliases()
	if _, ok := aliases[name]; !ok {
		fmt.Printf("Alias %q does not exist\n", name)
		return
	}
	fmt.Printf("Removed alias %q\n", name)
	delete(aliases, name)
	setAliases(aliases)
}

func GetAliases() map[string]string {
	if !utils.Exists(utils.AliasFile) {
		return map[string]string{}
	}

	contents, err := os.ReadFile(utils.AliasFile)
	if err != nil {
		log.Fatal(err)
	}

	aliases := map[string]string{}
	err = json.Unmarshal(contents, &aliases)
	if err != nil {
		log.Fatal(err)
	}

	return aliases
}

func setAliases(aliases map[string]string) {
	newAliases, err := json.MarshalIndent(aliases, "", "  ")
	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile(utils.AliasFile, newAliases, 0666)
	if err != nil {
		log.Fatal(err)
	}
}
