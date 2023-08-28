package gorinth

type ModeratorMessage struct {
	Message string `json:"message"`
	Body    string `json:"body"`
}

type License struct {
	Id   string `json:"id"`
	Name string `json:"name"`
	Url  string `json:"url"`
}

type GalleryImage struct {
	Url         string `json:"url"`
	Featured    bool   `json:"featured"`
	Title       string `json:"title"`
	Description string `json:"description"`
	Created     string `json:"created"`
	Ordering    int    `json:"ordering"`
}

type Dependency struct {
	VersionId      string `json:"version_id"`
	ProjectId      string `json:"project_id"`
	FileName       string `json:"file_name"`
	DependencyType string `json:"dependency_type"`
}

type File struct {
	Hashes struct {
		sha512 string
		sha1   string
	} `json:"hashes"`
	Url      string `json:"url"`
	Filename string `json:"filename"`
	Primary  bool   `json:"primary"`
	Size     int    `json:"size"`
	FileType string `json:"file_type"`
}

type PayoutData struct {
	Balance string `json:"balance"`
	PayoutWallet string `json:"payout_wallet"`
	PayoutWallerType string `json:"payout_wallet_type"`
	PayoutAddress string `json:"payout_address"`
}
