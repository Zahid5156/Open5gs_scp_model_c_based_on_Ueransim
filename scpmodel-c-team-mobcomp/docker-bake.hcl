variable "OPEN5GS_VERSION" {
  default = "v2.7.2"
}

variable "UERANSIM_VERSION" {
  default = "v3.2.6"
}

variable "UBUNTU_VERSION" {
  default = "jammy"
}

variable "NODE_VERSION" {
  default= "20"
}

group "default" {
  targets = ["base-open5gs", "amf", "ausf", "bsf", "nrf", "nssf",
              "pcf", "scp", "sepp", "smf", "udm", "udr", "upf", "webui", "base-ueransim", "gnb", "ue"]
}

target "base-ueransim" {
  context = "./images/base-ueransim"
  tags = ["base-ueransim:${UERANSIM_VERSION}"]
  output = ["type=image"]
}

target "gnb" {
  context = "./images/gnb"
  contexts = {
    "base-ueransim:${UERANSIM_VERSION}" = "target:base-ueransim"
  }
  tags = ["gnb:${UERANSIM_VERSION}"]
  output = ["type=image"]
}

target "ue" {
  context = "./images/ue"
  contexts = {
    "base-ueransim:${UERANSIM_VERSION}" = "target:base-ueransim"
  }
  tags = ["ue:${UERANSIM_VERSION}"]
  output = ["type=image"]
}

target "base-open5gs" {
  context = "./images/base-open5gs"
  tags = ["base-open5gs:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "amf" {
  context = "./images/amf"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["amf:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "ausf" {
  context = "./images/ausf"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["ausf:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "bsf" {
  context = "./images/bsf"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["bsf:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "nrf" {
  context = "./images/nrf"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["nrf:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "nssf" {
  context = "./images/nssf"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["nssf:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "pcf" {
  context = "./images/pcf"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["pcf:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "scp" {
  context = "./images/scp"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["scp:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "sepp" {
  context = "./images/sepp"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["sepp:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "smf" {
  context = "./images/smf"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["smf:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "udm" {
  context = "./images/udm"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["udm:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "udr" {
  context = "./images/udr"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["udr:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "upf" {
  context = "./images/upf"
  contexts = {
    "base-open5gs:${OPEN5GS_VERSION}" = "target:base-open5gs"
  }
  tags = ["upf:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}

target "webui" {
  context = "./images/webui"
  tags = ["webui:${OPEN5GS_VERSION}"]
  output = ["type=image"]
}