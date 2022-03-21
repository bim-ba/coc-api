class Methods:
    # clans
    CLANS = lambda: "/v1/clans"
    CLAN = lambda *, clantag: f"/v1/clans/{clantag}"
    CLAN_WARLOG = lambda *, clantag: f"/v1/clans/{clantag}/warlog"
    CLAN_MEMBERS = lambda *, clantag: f"/v1/clans/{clantag}/members"
    CLAN_CURRENT_WAR = lambda *, clantag: f"/v1/clans/{clantag}/currentwar"
    CLAN_CURRENT_WAR_LEAGUEGROUP = (
        lambda *, clantag: f"/v1/clans/{clantag}/currentwar/leaguegroup"
    )
    CLAN_CURRENT_LEAGUE_WAR = lambda *, wartag: f"/v1/clanwarleagues/wars/{wartag}"

    # players
    PLAYER = lambda *, playertag: f"/v1/players/{playertag}"
    PLAYER_VERIFY_API_TOKEN = (
        lambda *, playertag: f"/v1/players/{playertag}/verifytoken"
    )

    # leagues
    LEAGUES = lambda: "/v1/leagues"
    LEAGUE_INFO = lambda *, league_id: f"/v1/leagues/{league_id}"
    LEAGUE_SEASONS = lambda *, league_id: f"/v1/leagues/{league_id}/seasons"
    LEAGUE_SEASONS_RANKINGS = (
        lambda *, league_id, season_id: f"/v1/leagues/{league_id}/seasons/{season_id}"
    )
    WARLEAGUES = lambda: "warleagues"
    WARLEAGUE_INFORMATION = lambda *, league_id: f"warleagues/{league_id}"

    # locations
    LOCATIONS = lambda: "/v1/locations"
    LOCATION = lambda *, location_id: f"/v1/locations/{location_id}"

    # rankings
    CLAN_RANKINGS = lambda *, location_id: f"/v1/locations/{location_id}/rankings/clans"
    PLAYER_RANKINGS = (
        lambda *, location_id: f"/v1/locations/{location_id}/rankings/players"
    )
    CLAN_VERSUS_RANKINGS = (
        lambda *, location_id: f"/v1/locations/{location_id}/rankings/clans-versus"
    )
    PLAYER_VERSUS_RANKINGS = (
        lambda *, location_id: f"/v1/locations/{location_id}/rankings/players-versus"
    )

    # goldpass
    GOLDPASS = lambda: "/v1/goldpass/seasons/current"

    # labels
    CLAN_LABELS = lambda: "/v1/labels/clans"
    PLAYER_LABELS = lambda: "/v1/labels/players"
