import bencodepy


def get_torrent_name(path):
    try:
        with open(path, "rb") as f:
            data = bencodepy.decode(f.read())

        return data[b'info'][b'name'].decode("utf-8", errors="ignore")
    except:
        return None