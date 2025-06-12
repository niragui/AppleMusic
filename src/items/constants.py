from enum import Enum

RELATIONSHIPS_PARAMS = {}
RELATIONSHIPS_PARAMS["extend"] = "editorialArtwork,editorialVideo,offers,seoDescription,seoTitle,trackCount"
RELATIONSHIPS_PARAMS["fields[albums]"] = "name,artwork,playParams,url"
RELATIONSHIPS_PARAMS["fields[apple-curators]"] = "name,url"
RELATIONSHIPS_PARAMS["fields[artists]"] = "name,artwork,url"
RELATIONSHIPS_PARAMS["fields[curators]"] = "name,url"
RELATIONSHIPS_PARAMS["fields[songs]"] = "name,artistName,omposerName,albumName,trackNumber,discNumber,genreNames,durationInMillis,releaseDate,url,artistName,curatorName,composerName,artwork,playParams,contentRating,albumName,url,durationInMillis,audioTraits,extendedAssetUrls"
RELATIONSHIPS_PARAMS["include"] = "tracks,curator"
RELATIONSHIPS_PARAMS["include[music-videos]"] = "artists"
RELATIONSHIPS_PARAMS["include[songs]"] = "artists"
RELATIONSHIPS_PARAMS["l"] = "en-US"

class AppleTypes(Enum):
    PLAYLIST = "playlists"
    TRACK = "songs"
    ALBUM = "albums"
    ARTISTS = "artists"
    VIDEOS = "videos"