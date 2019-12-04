# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased] - yyyy-mm-dd

## [0.2.0] - 2019-12-04

### Added

- Webhooks returns HTTP status code and headers. This allows the implementation of rate limit handling.

### Changed

- Webhook.execute() now returns a response object instead of the send report. The response objects contains the HTTP status code, headers and content of the response from Discord (e.g. send report)

- Webhook.execute() wil no longer throw an exception on non 2xx HTTP codes. Instead the application code needs to investigate the status code that is returned. It will still through exceptions on all network related issues.

## [0.1.0] - 2019-11-12

### Added

- Initial
