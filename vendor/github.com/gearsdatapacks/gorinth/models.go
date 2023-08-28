package gorinth

type Project struct {
	Slug string `json:"slug"`
	Title string `json:"title"`
	Description string `json:"description"`
	Categories []string `json:"categories"`
	ClientSide string `json:"client_side"`
	ServerSide string `json:"server_side"`
	Body string `json:"body"`
	AdditionalCategories []string `json:"additional_categories"`
	IssuesUrl string `json:"issues_url"`
	SourceUrl string `json:"source_url"`
	WikiUrl string `json:"wiki_url"`
	DiscordUrl string `json:"discord_url"`
	DonationUrls []string `json:"donation_urls"`
	ProjectType string `json:"project_type"`
	Downloads int `json:"downloads"`
	IconUrl string `json:"icon_url"`
	Color int `json:"color"`
	Id string `json:"id"`
	Team string `json:"team"`
	ModeratorMessage ModeratorMessage `json:"moderator_message"`
	Published string `json:"published"`
	Updated string `json:"updated"`
	Approved string `json:"approved"`
	Followers int `json:"followers"`
	Status string `json:"status"`
	License License `json:"license"`
	Versions []string `json:"versions"`
	GameVersions []string `json:"game_versions"`
	Loaders []string `json:"loaders"`
	Gallery []GalleryImage `json:"gallery"`
	InitialVersions []map[string]any `json:"initial_versions"`
	auth string
}

type Version struct {
	Name string `json:"name"`
	VersionNumber string `json:"version_number"`
	Changelog string `json:"changelog"`
	Dependencies []Dependency `json:"dependencies"`
	GameVersions []string `json:"game_versions"`
	VersionType string `json:"version_type"`
	Loaders []string `json:"loaders"`
	Featured bool `json:"featured"`
	Status string `json:"status"`
	RequestedStatus string `json:"requested_status"`
	Id string `json:"id"`
	ProjectId string `json:"project_id"`
	AuthorId string `json:"author_id"`
	DatePublished string `json:"date_published"`
	Downloads int `json:"downloads"`
	Files []File `json:"files"`
	FileParts []string `json:"file_parts"`
}

type User struct {
	Username string `json:"username"`
	Name string `json:"name"`
	Email string `json:"email"`
	Bio string `json:"bio"`
	PayoutData PayoutData `json:"payout_data"`
	Id string `json:"id"`
	GithubId int `json:"github_id"`
	AvatarUrl string `json:"avatar_url"`
	Created string `json:"created"`
	Role string `json:"role"`
	Badges int8 `json:"badges"`
	auth string
}
