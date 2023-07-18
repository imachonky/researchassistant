from agentmemory import create_memory, get_memories, update_memory


def add_url_entry(
    url,
    text,
    context,
    type="url",
    valid=True,
    crawled=True
):
    project_name = context["project_name"]
    url_data = {"text": text, "url": url, "type": type, "project_name": project_name, "valid": valid, "crawled": crawled}
    create_memory(
        "scraped_urls",
        "url",
        url_data,
    )
    if context.get("scraped_urls", None) is None:
        context["scraped_urls"] = []
    context["scraped_urls"].append(url_data)
    return context


def get_entry_from_url(url):
    memory = get_memories("scraped_urls", filter_metadata={"url": url})
    memory = memory[0] if len(memory) > 0 else None
    return memory


def get_url_entries(context, valid=None, crawled=None):
    project_name = context["project_name"]
    # if valid and crawled are none, return all
    if valid is None and crawled is None:
        return get_memories("scraped_urls")
    dict = {
        "valid": valid,
        # TODO: we need to update agentmemory to enable these
        # "crawled": crawled,
        # "project_name": project_name
    }
    # if any values in dict are None, remove
    dict = {k: v for k, v in dict.items() if v is not None}
    return get_memories("scraped_urls", filter_metadata=dict)
    

def url_entry_exists(url):
    memory = get_entry_from_url(url)
    return memory is not None


def update_url_entry(
    url, text, valid=True, crawled=True, type="url", category="scraped_urls"
):
    update_memory(
        category, url, text, {"valid": valid, "crawled": crawled, "type": type}
    )


def url_has_been_crawled(url):
    memory = get_entry_from_url(url)
    if memory is None:
        return False
    return memory["metadata"]["crawled"]